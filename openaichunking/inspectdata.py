import chromadb

def inspect_chroma(db_path="Open_db"):
    # Initialize ChromaDB Persistent Client
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

if __name__ == "__main__":
    inspect_chroma("C:/Users/srira/Desktop/GenAi2/2newopen_db")
