from crewai import Task, Crew
from src.research_mind_agent.agents import reader_agent

read_task = Task(
    description="Scrape and summarize the content from https://blog.bytebytego.com/p/whats-next-in-ai-five-trends-to-watch",
    expected_output="A summary of the article's main points",
    agent=reader_agent,
)

crew = Crew(agents=[reader_agent], tasks=[read_task], verbose=True)
result = crew.kickoff()
print("\n\n=== RESULT ===")
print(result)