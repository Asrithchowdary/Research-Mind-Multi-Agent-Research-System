import os
from crewai import Agent, LLM
from dotenv import load_dotenv
from .tools import search_web, scrape_url

load_dotenv()

llm = LLM(
    model="ollama/qwen2.5:7b",
    base_url="http://localhost:11434/v1",
    api_key="ollama",
)

search_agent = Agent(
    role="Research Search Specialist",
    goal="Find the most credible, relevant and recent sources for a given research topic",
    backstory=(
        "You are an expert research assistant skilled at formulating precise "
        "search queries and identifying the most authoritative sources on any topic. "
        "You prioritize recent, credible references over outdated or low-quality ones."
    ),
    tools = [search_web],
    llm =llm,
    verbose=True,
)

reader_agent = Agent(
    role="Content Analyst",
    goal="Extract the single most valuable and detailed source from search results, then scrape its full content",
    backstory=(
        "You are a meticulous analyst who reviews search results, identifies the "
        "most promising and information-rich source, and extracts its full content "
        "for deeper analysis."
    ),
    tools=[scrape_url],
    llm=llm,
    verbose=True,
)