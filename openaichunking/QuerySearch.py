import os
import chromadb
import json
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables.")
openai.api_key = OPENAI_API_KEY


# Inspect ChromaDB collections
def inspect_chroma(db_path="Open_db"):
    client = chromadb.PersistentClient(path=db_path)

    print("Inspecting ChromaDB:")
    
    # Retrieve a list of collection names
    collection_names = client.list_collections()
    if not collection_names:
        print("No collections found in the database.")
        return

    # Print the total number of collections
    print(f"Total Collections: {len(collection_names)}")
    
    # List all collection names
    print("Collections:")
    for collection_name in collection_names:
        print(f"- {collection_name}")

    # Optionally, inspect each collection in detail
    for collection_name in collection_names:
        print(f"\nDetails of Collection: {collection_name}")
        collection = client.get_collection(collection_name)
        
        # Retrieve documents, metadata, and embeddings
        results = collection.get(include=["documents", "metadatas", "embeddings"])
        documents = results.get("documents", [])
        metadatas = results.get("metadatas", [])
        embeddings = results.get("embeddings", [])

        # Display collection details
        print(f"  Documents: {len(documents)}")
        if documents:
            print(f"  Sample Document: {documents[0][:50]}...")
        print(f"  Metadata: {len(metadatas)}")
        if metadatas:
            print(f"  Sample Metadata: {metadatas[0]}")
        print(f"  Embeddings: {len(embeddings)}")
        if len(embeddings) > 0:
            print(f"  Sample Embedding (first 10 values): {embeddings[0][:10]}")


# Search for documents in a collection
def search_chroma(client, collection_name, query_text, top_k=3):
    """
    Search for documents in a collection using a query.
    """
    collection = client.get_collection(collection_name)
    
    # Generate query embedding
    response = openai.Embedding.create(
        input=query_text,
        model="text-embedding-ada-002"
    )
    query_embedding = response['data'][0]['embedding']
    
    # Perform search
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )
    
    print(f"Search Results for '{query_text}' in collection '{collection_name}':")
    for i, doc in enumerate(results["documents"]):
        print(f"  Result {i + 1}: {doc[:50]}...")
        print(f"  Metadata: {results['metadatas'][i]}")
        print(f"  Distance: {results['distances'][i]}")
        print("=" * 50)



    
  


# Export a collection to a JSON file
def export_collection(client, collection_name, output_path):
    """
    Export a collection's data to a JSON file.
    """
    collection = client.get_collection(collection_name)
    results = collection.get(include=["documents", "metadatas", "embeddings"])
    
    # Convert embeddings to lists for JSON serialization
    embeddings = results.get("embeddings", [])
    embeddings_as_lists = [embedding.tolist() for embedding in embeddings]
    
    data = {
        "documents": results.get("documents", []),
        "metadatas": results.get("metadatas", []),
        "embeddings": embeddings_as_lists
    }
    
    # Save to JSON
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    
    print(f"Collection '{collection_name}' exported to {output_path}.")



# Main script
if __name__ == "__main__":
    db_path = "C:/Users/srira/Desktop/GenAi2/2newopen_db"
    client = chromadb.PersistentClient(path=db_path)

    # Inspect collections
    inspect_chroma(db_path)
    
    # Search example
    search_chroma(client, "industrypolicy", "growth policy", top_k=5)
    
    
    
    # Export example
    export_collection(client, "industrypolicy", "industrypolicy_backup.json")
