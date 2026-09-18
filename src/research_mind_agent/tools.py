import os
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
from crewai.tools import tool
from dotenv import load_dotenv

load_dotenv()

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

@tool("search_web")
def search_web(query: str) -> str:
    """Searches the web for a given and returns the top 5 results
    with titles,URLs, and snippets."""
    results = tavily_client.search(query, max_results =5)

    formatted = []
    for r in results.get("results", []):
        formatted.append(
            f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r['content'][:300]}"
        )
    return "\n\n".join(formatted)

@tool("scrape_url")
def scrape_url(url: str) -> str:
    """Scrapes the main text content from a given URL, stripping
    boilerplate like scripts, navigation, and footers."""
    try:
        response = requests.get(url, headers= HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()

        text = soup.get_text(separator=" ", strip=True)
        return text[:3000]
    except Exception as e:
        return f"Failed to scrape {url}: {str(e)}"

if __name__ == "__main__":
    print("=== Testing search_web ===")
    print(search_web.run("latest devolpments in AI Agents 2026"))

    print("\n=== Testing scrape_url ===")
    print(scrape_url.run("https://en.wikipedia.org/wiki/Artificial_intelligence"))