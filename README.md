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

## Requirements
1. **Python Version**: Python 3.8 or higher.
2. **Dependencies**:
   Install required libraries using:
   ```bash
   pip install watchdog PyPDF2 python-docx chromadb pandas sentence-transformers
