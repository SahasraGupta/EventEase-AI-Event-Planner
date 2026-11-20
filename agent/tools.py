from langchain_core.tools import tool
from rag_pipeline.retriever import get_retriever
from rag_pipeline.web_search import search_web
from rag_pipeline.web_scrap import scrape_web
from rag_pipeline.web_pipeline import fetch_web_content


@tool
def retrieve_documents(query:str):
    """Retrieve relevant event-planning information from the ChromaDB vector database."""
    retriever=get_retriever()
    documents=retriever.invoke(query)
    for i, doc in enumerate(documents, start=1):
        print(f"\nCHUNK {i}")
        print("SOURCE:", doc.metadata.get("source"))
        print("CONTENT LENGTH:", len(doc.page_content))
        print("CONTENT:", doc.page_content[:1000])
    context="\n\n".join(
        doc.page_content[:1500] for doc in documents
    )
    return context

@tool
def search_and_scrap(query: str):
    """Search the web, scrape content, and retrieve relevant information."""
    vector_store,source_urls=fetch_web_content(query)
    retriever=get_retriever(source_urls)
    documents=retriever.invoke(query)

    for i, doc in enumerate(documents, start=1):
        print(f"\n--- CHUNK {i} ---")
        print("SOURCE:", doc.metadata.get("source"))
        print("CONTENT PREVIEW:", doc.page_content[:500])
    context="\n\n".join(doc.page_content[:1500]
                    for doc in documents
    )
    return context