from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

def split_documents(scraped_content):

    documents = []

    for result in scraped_content["results"]:

        document = Document(
            page_content=result["raw_content"],
            metadata={
                "source": result["url"]
            }
        )

        documents.append(document)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(documents)#only splits page content

    return chunks