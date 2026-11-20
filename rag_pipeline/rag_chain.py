from rag_pipeline.retriever import get_retriever
from rag_pipeline.llm import get_llm
from langchain_core.prompts import ChatPromptTemplate
from rag_pipeline.web_pipeline import fetch_web_content

def get_rag_chain(user_query):

    fetch_web_content(user_query)
    retriever=get_retriever()
    llm=get_llm()
    retrieved_docs=retriever.invoke(user_query)

    prompt=ChatPromptTemplate.from_template("""
    You are AI event planner.
    Answer the user's questions using the following content.

    Context:
    {context}
    User question:
    {question}

    If the answer is not available in the context,clearly say that

    """)

    doc_content="\n\n".join(doc.page_content
        for doc in retrieved_docs
    )
    formated_prompt=prompt.invoke({
        "context":doc_content,
        "question":user_query
    })
    response=llm.invoke(formated_prompt)
    return response.content
