import os
import re
from PyPDF2 import PdfReader
import pdfplumber
import spacy
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans


def create_folder(base_folder, pdf_name, chunk_type):
    # Create a directory for the PDF and the chunk type
    folder_path = os.path.join(base_folder, pdf_name, chunk_type)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path


def save_chunk(folder_path, chunk_name, content):
    # Save content to a text file only if it doesn't already exist
    file_path = os.path.join(folder_path, f"{chunk_name}.txt")
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)


def chunk_pdf(pdf_path, output_folder):
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    reader = PdfReader(pdf_path)
    nlp = spacy.load("en_core_web_sm")

    # **1. Page-Wise Chunking**
    page_folder = create_folder(output_folder, pdf_name, "page_chunks")
    for page_num, page in enumerate(reader.pages):
        content = page.extract_text()
        save_chunk(page_folder, f"page_{page_num + 1}", content)

    # **2. Paragraph-Wise Chunking**
    paragraph_folder = create_folder(output_folder, pdf_name, "paragraph_chunks")
    for page_num, page in enumerate(reader.pages):
        text = page.extract_text()
        paragraphs = re.split(r'\n\s*\n', text)
        for i, paragraph in enumerate(paragraphs):
            save_chunk(paragraph_folder, f"page_{page_num + 1}_paragraph_{i + 1}", paragraph)

    # **3. Sentence-Wise Chunking**
    sentence_folder = create_folder(output_folder, pdf_name, "sentence_chunks")
    for page_num, page in enumerate(reader.pages):
        text = page.extract_text()
        doc = nlp(text)
        for i, sentence in enumerate(doc.sents):
            save_chunk(sentence_folder, f"page_{page_num + 1}_sentence_{i + 1}", sentence.text)

    # **4. Table-Based Chunking**
    table_folder = create_folder(output_folder, pdf_name, "table_chunks")
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            tables = page.extract_tables()
            for table_num, table in enumerate(tables):
                # Handle None values in the table
                table_text = "\n".join(["\t".join(cell if cell is not None else "" for cell in row) for row in table])
                save_chunk(table_folder, f"page_{page_num + 1}_table_{table_num + 1}", table_text)

    # **5. Fixed-Size Chunking**
    fixed_chunk_folder = create_folder(output_folder, pdf_name, "fixed_size_chunks")
    for page_num, page in enumerate(reader.pages):
        text = page.extract_text()
        words = text.split()
        chunk_size = 100
        for i in range(0, len(words), chunk_size):
            chunk_text = " ".join(words[i:i + chunk_size])
            save_chunk(fixed_chunk_folder, f"page_{page_num + 1}_chunk_{i // chunk_size + 1}", chunk_text)

    # **6. Keyword-Based Chunking**
    keyword_folder = create_folder(output_folder, pdf_name, "keyword_chunks")
    keywords = ["Introduction", "Conclusion", "References"]
    for page_num, page in enumerate(reader.pages):
        text = page.extract_text()
        for keyword in keywords:
            if keyword in text:
                chunk = text.split(keyword, 1)[1]
                save_chunk(keyword_folder, f"page_{page_num + 1}_keyword_{keyword}", chunk)

    # **7. Section-Wise Chunking**
    section_folder = create_folder(output_folder, pdf_name, "section_chunks")
    full_text = "\n".join([page.extract_text() for page in reader.pages])
    sections = re.split(r'(Chapter \d+|Section \d+)', full_text)
    for i, section in enumerate(sections):
        save_chunk(section_folder, f"section_{i + 1}", section.strip())

    # **8. Semantic Chunking**
    semantic_folder = create_folder(output_folder, pdf_name, "semantic_chunks")
    sentences = []
    for page in reader.pages:
        sentences.extend(page.extract_text().split("."))
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(sentences)
    kmeans = KMeans(n_clusters=3).fit(embeddings)
    for cluster_id in range(3):
        cluster_sentences = [sentences[i] for i in range(len(sentences)) if kmeans.labels_[i] == cluster_id]
        save_chunk(semantic_folder, f"cluster_{cluster_id + 1}", "\n".join(cluster_sentences))

    # **9. Visual Element-Based Chunking**
    visual_folder = create_folder(output_folder, pdf_name, "visual_chunks")
    doc = pdfplumber.open(pdf_path)
    for page_num, page in enumerate(doc.pages):
        images = page.images
        save_chunk(visual_folder, f"page_{page_num + 1}_visual_info", str(images))

    print(f"Chunking completed for {pdf_name}. Check the folder: {output_folder}")


# **Run the script**
if __name__ == "__main__":
    pdf_path = "C:/Users/srira/Desktop/GenAi2/RAG/AI.pdf"  # Replace with your PDF file path
    output_folder = "9typeschunked_pdfs"  # Base output folder

    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Chunk the PDF
    chunk_pdf(pdf_path, output_folder)
