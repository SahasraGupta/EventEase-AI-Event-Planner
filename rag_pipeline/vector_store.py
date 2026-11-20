from langchain_chroma import Chroma
from rag_pipeline.embeddings import get_embedding_model


def store_documents(chunks, source_urls):
    embedding_model = get_embedding_model()

    vector_store = Chroma(
        collection_name="event_planner",
        persist_directory="./data/vector_store",
        embedding_function=embedding_model
    )

    # Remove previously stored chunks from the same URLs
    for url in source_urls:
        vector_store.delete(
            where={"source": url}
        )

    # Store fresh chunks
    vector_store.add_documents(chunks)

    return vector_store