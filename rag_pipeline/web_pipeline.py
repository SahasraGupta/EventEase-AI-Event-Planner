from rag_pipeline.web_search import search_web
from rag_pipeline.web_scrap import scrape_web
from rag_pipeline.chunking import split_documents
from rag_pipeline.vector_store import store_documents


def fetch_web_content(query: str):
    # Step 1: Search the web
    search_results = search_web(query)

    urls = [
        result["url"]
        for result in search_results["results"]
    ]



    # Step 2: Scrape webpage content
    scraped_content = scrape_web(urls)

    # Step 3: Split scraped content into chunks
    chunks = split_documents(scraped_content)

    # Step 4: Remove old chunks and store fresh chunks
    vector_store = store_documents(chunks, urls)

    return vector_store, urls