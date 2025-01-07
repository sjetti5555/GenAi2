import chromadb
import openai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in .env file.")

openai.api_key = OPENAI_API_KEY

def query_chroma(collection_name, query_text, db_path="Open_db"):
    """
    Query ChromaDB for documents similar to the provided query text.
    """
    client = chromadb.PersistentClient(path=db_path)
    collection = client.get_collection(collection_name)

    # Generate embedding for the query text
    response = openai.Embedding.create(
        input=query_text,
        model="text-embedding-ada-002"
    )
    query_embedding = response['data'][0]['embedding']

    # Query the collection
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3,  # Return top 3 results
        include=["documents", "metadatas", "distances"]  # Valid fields only
    )

    print("Query Results:")
    for i, doc in enumerate(results["documents"]):
        print(f"Result {i + 1}: {doc[:50]}...")
        print(f"Metadata: {results['metadatas'][i]}")
        print(f"Distance: {results['distances'][i]}")
        print("=" * 50)

if __name__ == "__main__":
    query_text = " industry growth and market trends"
    query_chroma("growth", query_text, "newopen_db")
