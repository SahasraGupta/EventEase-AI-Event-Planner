from rag_pipeline.retriever import get_retriever

query = "Suggest birthday party venues in Hyderabad for 100 guests."

retriever = get_retriever()

documents = retriever.invoke(query)

print("Number of retrieved documents:", len(documents))

for doc in documents:
    print("\nContent:", doc.page_content[:300])
    print("Source:", doc.metadata)