from dotenv import load_dotenv
from langchain_tavily import TavilyExtract

load_dotenv()

def scrape_web(urls :list[str]):
    extract_tool=TavilyExtract(
        extract_depth="basic",
        format="markdown"#extracted content in which format it should be represented
    )
    results=extract_tool.invoke({
        "urls":urls
    })
    return results