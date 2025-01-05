import chromadb

def inspect_chroma(db_path="chroma_db"):
    client = chromadb.PersistentClient(path=db_path)

    print("Listing all stored collections and their data:")
    # List all collection names
    collection_names = client.list_collections()
    if not collection_names:
        print("No collections found in the database.")
        return

    for collection_name in collection_names:
        print(f"Collection: {collection_name}")
        
        # Access the collection
        collection = client.get_collection(collection_name)
        results = collection.get(include=["documents", "metadatas"])
        
        doc_count = len(results["documents"])
        if doc_count == 0:
            print(f"No documents found in collection: {collection_name}.")
        else:
            print(f"{doc_count} documents found in collection: {collection_name}.")
            for i, doc in enumerate(results["documents"]):
                print(f"Document {i + 1}: {doc[:100]}...")  # Display first 100 characters
                print(f"Metadata: {results['metadatas'][i]}")
                print("=" * 50)

# Run inspection
if __name__ == "__main__":
    inspect_chroma("chroma_db")
