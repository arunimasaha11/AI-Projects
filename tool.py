from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os 
from dotenv import load_dotenv
from rich import print 
load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool 
def web_search(query : str) -> str:
    """Search the web for recent and reliable information on a topic. Returns titles, URLs and snippets."""
    results = tavily.search(query=query,max_results=5)
    out = []    
    for r in results['results']:
        out.append(
            f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r['content'][:500]}\n"
        )
        
    return "\n******************\n".join(out)

# print(web_search.invoke("what are the recent updates on Strait of Hormuz opening?"))

@tool
def scrape_url(url: str) ->str :
    """Scrape and return clean content from a given URL for deeper readings"""
    try:
        resp = requests.get(url,timeout=10,headers={"User-Agent":"Google Chrome"})
        soup = BeautifulSoup(resp.text,"html.parser")
        for tag in soup(["script","style","nav","footer"]):
            tag.decompose()
        return soup.get_text(separator=" ", strip=True)[:3000]
    except Exception as e:
        return f"Could not scrape the URL: {str(e)}"
    
# print(scrape_url.invoke("https://www.wired.com/story/the-strait-of-hormuz-reopens-but-global-shipping-will-take-months-to-recover/"))