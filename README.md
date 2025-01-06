GenAi2
ChromaDB Document Chunking and Embedding
This project monitors a folder for new or modified files, extracts text, chunks it, generates embeddings, and stores the data in a ChromaDB vector database. It dynamically creates collections in ChromaDB based on file names and avoids duplicate entries.

Features
✅ File Monitoring:
Watches a specific folder for new or modified files using watchdog.
✅ Supported File Types:
.txt, .pdf, .docx, .csv, .xlsx.
✅ Text Chunking:
Splits the text into smaller chunks (default: 500 characters).
✅ Vector Embedding:
Uses Sentence Transformers (all-MiniLM-L6-v2) or OpenAI embeddings (text-embedding-ada-002).
✅ Dynamic Collection Creation:
Automatically creates a new ChromaDB collection based on the file name.
✅ Deduplication:
Ensures no duplicate data is stored in ChromaDB.
✅ Real-Time Logs:
Logs details of processed files, chunk generation, and embedding creation.
✅ Inspection Script:
Lists all collections and their stored data for debugging and verification.
RAG Folder Contents
📁 A. 3typedchunking
Description: This folder contains scripts for chunking documents using three methods:
📄 Page-Wise Chunking:
Splits the document into chunks by individual pages.
Saves each page as a .txt file.
📄 Paragraph-Wise Chunking:
Splits the content into paragraphs using newline delimiters.
Saves each paragraph as a .txt file.
📄 Sentence-Wise Chunking:
Tokenizes the document into sentences using spaCy.
Saves each sentence as a .txt file.
Scripts:
3typedpdfchunking.py: Combines all three chunking methods.
pagewise.py: Focuses on page-wise chunking.
paragraphwise.py: Focuses on paragraph-wise chunking.
📁 B. 9typedchunking
Description: This folder contains a script supporting 9 advanced chunking methods:
📄 Page-Wise Chunking.
📄 Paragraph-Wise Chunking.
📄 Sentence-Wise Chunking.
📊 Table-Based Chunking:
Extracts tables using pdfplumber.
Saves tabular data as .txt files.
📏 Fixed-Size Chunking:
Splits text into fixed-size chunks (default: 100 words).
🗝️ Keyword-Based Chunking:
Extracts content based on specific keywords.
📚 Section-Wise Chunking:
Splits content based on section headers.
🧠 Semantic Chunking:
Groups sentences based on semantic similarity using KMeans.
🖼️ Visual Element-Based Chunking:
Extracts images and visual elements from the document.
Script:
9TypePDFChunking.py: Implements all the above chunking techniques.
📁 C. Test Files
Description: Sample files for testing chunking scripts:
📄 andhra.docx: Example Word document.
📄 andhra.pdf: Example PDF document.
📄 andhra.txt: Example text file.
📁 chunking
Description: Contains scripts for SentenceTransformer-based embedding.
Scripts:
docchunking_sentanceemb.py: Monitors a folder, processes documents, and stores results in ChromaDB.
inspect_Chroma.py: Inspects ChromaDB collections and lists stored data.
query_Chroma.py: Queries ChromaDB for relevant documents.
📁 openaichunking
Description: Contains scripts for OpenAI-based embedding.
Scripts:
docchunking_sentanceemb.py: Monitors a folder, processes documents, and stores results in an OpenAI-powered database.
inspect_Opendb.py: Inspects stored collections in the OpenAI-powered database.
query_Opendb.py: Queries the OpenAI-powered database for relevant documents.
Logs
📝 processing.log: Tracks activities related to SentenceTransformer-based processing.
📝 processing1.log: Tracks activities related to OpenAI-based processing.
Setup Instructions
🛠️ 1. Install Dependencies
Install all required Python libraries:

bash
Copy code
pip install watchdog PyPDF2 python-docx chromadb pandas sentence-transformers openai pdfplumber
🛠️ 2. Run Document Processing
A. SentenceTransformer-Based Embedding
Navigate to the chunking/ folder.
Run the following command:
bash
Copy code
python docchunking_sentanceemb.py
Add files to the monitored folder for real-time processing.
B. OpenAI-Based Embedding
Navigate to the openaichunking/ folder.
Set up a .env file with your OpenAI API key:
plaintext
Copy code
OPENAI_API_KEY=sk-your-openai-api-key
Run the following command:
bash
Copy code
python docchunking_sentanceemb.py
Add files to the monitored folder for real-time processing.
🛠️ 3. Inspect Stored Data
ChromaDB (SentenceTransformer)
Run:

bash
Copy code
python inspect_Chroma.py
OpenAI-Powered Database
Run:

bash
Copy code
python inspect_Opendb.py
🛠️ 4. Query Stored Data
ChromaDB (SentenceTransformer)
Run:

bash
Copy code
python query_Chroma.py
OpenAI-Powered Database
Run:

bash
Copy code
python query_Opendb.py
