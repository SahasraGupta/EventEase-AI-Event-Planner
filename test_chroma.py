import chromadb

client = chromadb.PersistentClient(
    path="./data/chroma_test"
)

collection = client.get_or_create_collection(
    name="test_collection"
)

print("ChromaDB initialized successfully!")