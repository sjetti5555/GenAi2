# GenAi2
# ChromaDB Document Chunking and Embedding

This project monitors a folder for new or modified files, extracts text, chunks it, generates embeddings, and stores the data in a ChromaDB vector database. It dynamically creates collections in ChromaDB based on the file names and avoids duplicate entries.

## Features
1. **File Monitoring**:
   - Watches a specific folder for new or modified files using `watchdog`.
2. **Supported File Types**:
   - `.txt`, `.pdf`, `.docx`, `.csv`, `.xlsx`.
3. **Text Chunking**:
   - Splits the text into smaller chunks (default: 500 characters).
4. **Vector Embedding**:
   - Uses Sentence Transformers (`all-MiniLM-L6-v2`) to generate embeddings.
5. **Dynamic Collection Creation**:
   - Automatically creates a new ChromaDB collection based on the file name.
6. **Deduplication**:
   - Checks for existing documents in ChromaDB before adding new data.
7. **Real-Time Logs**:
   - Provides detailed logs for processed files, chunk generation, and embedding creation.
8. **Inspection Script**:
   - Lists all collections and their stored data for debugging and verification.

---


---
# RAG Folder Contains The Following:

#### **A. 3typeppdfchunking**
This folder contains Python file chunking with 3 methods:
- **Page-Wise Chunking**:
  - Splits the document into chunks by individual pages.
  - Saves each page as a `.txt` file.
- **Paragraph-Wise Chunking**:
  - Splits the content into paragraphs using newline delimiters.
  - Saves each paragraph as a `.txt` file.
- **Sentence-Wise Chunking**:
  - Tokenizes the document into sentences using `spaCy`.
  - Saves each sentence as a `.txt` file.


#### **B. 9typedpdfchunking**
This folder contains Python file  chunking with 9 methods:

1. **Page-Wise Chunking**.
2. **Paragraph-Wise Chunking**.
3. **Sentence-Wise Chunking**.
4. **Table-Based Chunking**:
   - Extracts tables from PDFs using `pdfplumber`.
   - Saves tabular data in `.txt` files.
5. **Fixed-Size Chunking**:
   - Splits content into chunks of a fixed word count (default: 100 words).
6. **Keyword-Based Chunking**:
   - Extracts content following specific keywords (e.g., "Introduction").
7. **Section-Wise Chunking**:
   - Splits content based on section headers (e.g., "Chapter 1").
8. **Semantic Chunking**:
   - Groups sentences into clusters based on semantic similarity using KMeans.
9. **Visual Element-Based Chunking**:
   - Extracts images and visual elements from the document.

---

## Test Files
- **andhra.pdf**:
  - Example PDF for testing all chunking workflows.
- **andhra.doc**:
  - Example Word document for testing paragraph and sentence-wise chunking.
- **andhra.txt**:
  - Example text file for testing paragraph and sentence-wise chunking.

---


## Requirements
1. **Python Version**: Python 3.8 or higher.
2. **Dependencies**:
   Install required libraries using:
   ```bash
   pip install watchdog PyPDF2 python-docx chromadb pandas sentence-transformers
