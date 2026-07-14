from langchain.tools import tool
import requests
from tavily import TavilyClient
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
load_dotenv()

tavily_client = TavilyClient(api_key=os.getenv("tavily"))

@tool
def web_search(query: str) -> str:
    """Performs a web search using Tavily API and Find the recent information on a Topic."""
    response = tavily_client.search(query=query,max_results=5)
    out=[]
    for i in response['results']:
        out.append(f"title: {i['title']}\n url: {i['url']}\n")
        out.append("-" * 50)
    return "\n".join(out)
    
@tool
def scrape_url(url:str) ->str:
    """Scrapes a website and returns the content"""
    try:
        res=requests.get(url,timeout=8,headers={'User-Agent' : 'Mozilla/5.0'})
        soup=BeautifulSoup(res.content,'html.parser')
        for script in soup(['script','style','nav','footer','aside','header','form']):
            script.decompose()
        return soup.get_text(separator='\n',strip=True)[:4000]
    except Exception as e:
        return f"Error scraping website {url}: {e}"

    