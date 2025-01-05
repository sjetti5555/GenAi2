import os
import re
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PyPDF2 import PdfReader
from docx import Document
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import pandas as pd

# **Utility Functions**
def extract_text(file_path):
    text = ""
    if file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
    elif file_path.endswith(".pdf"):
        reader = PdfReader(file_path)
        for page in reader.pages:
            text += page.extract_text()
    elif file_path.endswith(".docx"):
        doc = Document(file_path)
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
    elif file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
        text = df.to_string(index=False)
    elif file_path.endswith(".xlsx"):
        df = pd.read_excel(file_path)
        text = df.to_string(index=False)
    return text

def chunk_text(text, chunk_size=100):
    chunks = []
    paragraphs = re.split(r'\n\s*\n', text)
    for paragraph in paragraphs:
        while len(paragraph) > chunk_size:
            chunks.append(paragraph[:chunk_size])
            paragraph = paragraph[chunk_size:]
        chunks.append(paragraph)
    print(f"Chunked text into {len(chunks)} chunks.")
    return chunks

    


def embed_chunks(chunks):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(chunks)
    return embeddings

def store_in_chroma(file_name, chunks, embeddings, db_path="chroma_db"):
    # Initialize ChromaDB Persistent Client
    client = chromadb.PersistentClient(path=db_path)
    
    # Use the file name (without extension) as the collection name
    collection_name = os.path.splitext(os.path.basename(file_name))[0]
    collection = client.get_or_create_collection(collection_name)

    # Add chunks and embeddings to ChromaDB
    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        # Query to check for existing documents to avoid duplication
        existing_docs = collection.query(query_texts=[chunk], n_results=1)["documents"]
        if not existing_docs:  # Only add if not already present
            collection.add(
                ids=[f"{collection_name}_chunk_{i}"],
                metadatas=[{"source": file_name}],
                documents=[chunk],
                embeddings=[embedding]
            )
            print(f"Added chunk {i} to collection {collection_name}: {chunk[:50]}...")
        else:
            print(f"Duplicate chunk {i}, not added: {chunk[:50]}...")
    print(f"Data from {file_name} successfully stored in ChromaDB as {collection_name}.")


# **Folder Monitoring**
class FolderHandler(FileSystemEventHandler):
    def __init__(self, folder_to_monitor, db_path):
        self.folder_to_monitor = folder_to_monitor
        self.db_path = db_path
        self.processed_files = {}
        self.last_file_processed_time = time.time()

    def on_modified(self, event):
        if event.is_directory:
            return
        file_path = event.src_path
        if file_path.endswith((".txt", ".pdf", ".docx", ".csv", ".xlsx")):
            self.process_file(file_path)

    def on_created(self, event):
        self.on_modified(event)

    def process_file(self, file_path):
        last_modified_time = os.path.getmtime(file_path)
        if file_path not in self.processed_files or self.processed_files[file_path] < last_modified_time:
            self.processed_files[file_path] = last_modified_time
            self.last_file_processed_time = time.time()
            print(f"Processing: {file_path}")

            text = extract_text(file_path)
            print(f"Extracted text from {os.path.basename(file_path)}.")
            chunks = chunk_text(text)
            embeddings = embed_chunks(chunks)
            store_in_chroma(file_path, chunks, embeddings, self.db_path)

# **Main Script**
if __name__ == "__main__":
    folder_to_monitor = "C:/Users/srira/Desktop/GenAi2/RAG/chunking"  # Replace with your folder path
    db_path = "chroma_db"  # Path to store the Chroma DB

    # Initialize folder monitoring
    event_handler = FolderHandler(folder_to_monitor, db_path)
    observer = Observer()
    observer.schedule(event_handler, folder_to_monitor, recursive=True)

    print(f"Monitoring folder: {folder_to_monitor}")

    try:
        observer.start()
        while True:
            time.sleep(15)  # Print log every 15 seconds
            time_since_last_file = time.time() - event_handler.last_file_processed_time
            if time_since_last_file >= 15:
                print("No new files have been added recently. Waiting for new files to process...")
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
