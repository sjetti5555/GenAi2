# **GenAi2**
## **ChromaDB Document Chunking and Embedding**

This project monitors a folder for new or modified files, extracts text, chunks it, generates embeddings, and stores the data in a ChromaDB vector database. It dynamically creates collections in ChromaDB based on file names and avoids duplicate entries.

---

## **Features**

✅ **File Monitoring**:  
   - Watches a specific folder for new or modified files using `watchdog`.

✅ **Supported File Types**:  
   - `.txt`, `.pdf`, `.docx`, `.csv`, `.xlsx`.

✅ **Text Chunking**:  
   - Splits the text into smaller chunks (default: 500 characters).

✅ **Vector Embedding**:  
   - Uses Sentence Transformers (`all-MiniLM-L6-v2`) or OpenAI embeddings (`text-embedding-ada-002`).

✅ **Dynamic Collection Creation**:  
   - Automatically creates a new ChromaDB collection based on the file name.

✅ **Deduplication**:  
   - Ensures no duplicate data is stored in ChromaDB.

✅ **Real-Time Logs**:  
   - Logs details of processed files, chunk generation, and embedding creation.

✅ **Inspection Script**:  
   - Lists all collections and their stored data for debugging and verification.

---

## **RAG Folder Contents**

### 📁 **A. 3typedchunking**
**Description**: This folder contains scripts for chunking documents using three methods:  
- 📄 **Page-Wise Chunking**:  
   - Splits the document into chunks by individual pages.  
   - Saves each page as a `.txt` file.
- 📄 **Paragraph-Wise Chunking**:  
   - Splits the content into paragraphs using newline delimiters.  
   - Saves each paragraph as a `.txt` file.
- 📄 **Sentence-Wise Chunking**:  
   - Tokenizes the document into sentences using `spaCy`.  
   - Saves each sentence as a `.txt` file.

**Scripts**:  
- `3typedpdfchunking.py`: Combines all three chunking methods.  
- `pagewise.py`: Focuses on page-wise chunking.  
- `paragraphwise.py`: Focuses on paragraph-wise chunking.  

---

### 📁 **B. 9typedchunking**
**Description**: This folder contains a script supporting 9 advanced chunking methods:  
1. 📄 **Page-Wise Chunking**.  
2. 📄 **Paragraph-Wise Chunking**.  
3. 📄 **Sentence-Wise Chunking**.  
4. 📊 **Table-Based Chunking**:  
   - Extracts tables using `pdfplumber`.  
   - Saves tabular data as `.txt` files.  
5. 📏 **Fixed-Size Chunking**:  
   - Splits text into fixed-size chunks (default: 100 words).  
6. 🗝️ **Keyword-Based Chunking**:  
   - Extracts content based on specific keywords.  
7. 📚 **Section-Wise Chunking**:  
   - Splits content based on section headers.  
8. 🧠 **Semantic Chunking**:  
   - Groups sentences based on semantic similarity using KMeans.  
9. 🖼️ **Visual Element-Based Chunking**:  
   - Extracts images and visual elements from the document.

**Script**:  
- `9TypePDFChunking.py`: Implements all the above chunking techniques.

---

### 📁 **C. Test Files**
**Description**: Sample files for testing chunking scripts:  
- 📄 `Andhra_Pradesh_IEEE_Formatted (1).docx`      : Example Word document. 
- 📄 `Data Science for Industrial Policy.pptx`     : Example pptx file.  
- 📄 `Data-Driven Insights for Industry Growth.pdf`: Example PDF document. 
- 📄 `math module.xlsx`                            : Example xlsx file.   
- 📄 `Number of approaches to Re-use Module.txt`   : Example text file.  

---

### 📁 **chunking**
**Description**: Contains scripts for SentenceTransformer-based embedding.  

**Scripts**:  
- `docchunking_sentanceemb.py`:  
   - Monitors a folder, processes documents, and stores results in ChromaDB.  
- `inspect_Chroma.py`:  
   - Inspects ChromaDB collections and lists stored data.  
- `query_Chroma.py`:  
   - Queries ChromaDB for relevant documents.  

---

### 📁 **openaichunking**
**Description**: Contains scripts for OpenAI-based embedding.  

**Scripts**:  
- `docchunking_sentanceemb.py`:  
   - Monitors a folder, processes documents, and stores results in an OpenAI-powered database.  
- `inspect_Opendb.py`:  
   - Inspects stored collections in the OpenAI-powered database.  
- `query_Opendb.py`:  
   - Queries the OpenAI-powered database for relevant documents.  


---

## **Setup Instructions**

### 🛠️ **1. Install Dependencies**
Install all required Python libraries:
```bash
pip install watchdog PyPDF2 python-docx chromadb pandas sentence-transformers openai pdfplumber
