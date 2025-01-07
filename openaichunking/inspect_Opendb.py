import chromadb

def inspect_chroma(db_path="Open_db"):
    client = chromadb.PersistentClient(path=db_path)

    print("Listing all stored collections and their data:")
    collection_names = client.list_collections()
    if not collection_names:
        print("No collections found in the database.")
        return

    for collection_name in collection_names:
        print(f"Collection: {collection_name}")
        collection = client.get_collection(collection_name)

        # Retrieve all documents, metadatas, and embeddings
        results = collection.get(include=["documents", "metadatas", "embeddings"])
        documents = results.get("documents", [])
        metadatas = results.get("metadatas", [])
        embeddings = results.get("embeddings", [])

        if not documents:
            print(f"No documents found in collection: {collection_name}.")
        else:
            print(f"{len(documents)} documents found in collection: {collection_name}.")
            for i, doc in enumerate(documents):
                print(f"Document {i + 1}: {doc[:10]}...")
                print(f"Metadata: {metadatas[i]}")
                print(f"Embedding (first 5 values): {embeddings[i][:5]}")
                print("=" * 10)

if __name__ == "__main__":
    inspect_chroma("C:/Users/srira/Desktop/GenAi2/2newopen_db")
