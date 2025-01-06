import chromadb
from sentence_transformers import SentenceTransformer

def query_chroma(collection_name, query_text, db_path="Chroma_db"):
    """
    Query ChromaDB for documents similar to the provided query text.
    """
    # Initialize ChromaDB client
    client = chromadb.PersistentClient(path=db_path)
    collection = client.get_collection(collection_name)

    # Generate embedding for the query text using SentenceTransformer
    model = SentenceTransformer("all-MiniLM-L6-v2")
    query_embedding = model.encode([query_text])[0]

    # Query the collection
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3,  # Return top 3 results
        include=["documents", "metadatas", "distances"]  # Valid fields only
    )

    # Display the query results
    print("Query Results:")
    for i, doc in enumerate(results["documents"]):
        print(f"Result {i + 1}: {doc[:50]}...")
        print(f"Metadata: {results['metadatas'][i]}")
        print(f"Distance: {results['distances'][i]}")
        print("=" * 50)

if __name__ == "__main__":
    # Replace with your query text
    query_text = "Nara Chandrababu Naidu"
    query_chroma("andhra", query_text, "Chroma_db")
