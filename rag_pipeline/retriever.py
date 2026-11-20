
from langchain_chroma import Chroma
from rag_pipeline.embeddings import get_embedding_model

def get_retriever(source_urls=None):
    #In retrieve_documents tool we wont send urls
    #In search_and_scrap we pass the urls so its optional we kept None
    embedding_model = get_embedding_model()

    vector_store = Chroma(
        collection_name="event_planner",
        persist_directory="./data/vector_store",
        embedding_function=embedding_model
    )

    search_kwargs = {"k": 10}

    if source_urls:
        search_kwargs["filter"] = {
            "source": {"$in": source_urls}
        }

    retriever = vector_store.as_retriever(
        search_kwargs=search_kwargs
    )

    return retriever
