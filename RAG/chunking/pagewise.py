import os
import re
from PyPDF2 import PdfReader
import pdfplumber
import spacy


def create_folder(base_folder, pdf_name, chunk_type):
    # Create a directory for the PDF and the chunk type
    folder_path = os.path.join(base_folder, pdf_name, chunk_type)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path


def save_chunk(folder_path, chunk_name, content):
    # Save content to a text file
    file_path = os.path.join(folder_path, f"{chunk_name}.txt")
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

    print(f"Chunking completed for {pdf_name}. Check the folder: {output_folder}")

    # **Run the script**
if __name__ == "__main__":
      pdf_path = "C:/Users/srira/Desktop/GenAi2/RAG/AI.pdf"  # Replace with your PDF file path
      output_folder = "pagewise_pdfs"     # Base output folder

    # Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

    # Chunk the PDF
chunk_pdf(pdf_path, output_folder)