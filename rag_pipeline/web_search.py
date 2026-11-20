from dotenv import load_dotenv
from langchain_tavily import TavilySearch

load_dotenv()

def search_web(query:str):
    search_tool=TavilySearch(max_results=10)
    results=search_tool.invoke({
        "query":query
    })
    return results