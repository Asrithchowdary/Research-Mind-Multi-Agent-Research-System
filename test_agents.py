from crewai import Task, Crew
from src.research_mind_agent.agents import search_agent, reader_agent

search_task = Task(
    description="Search for information about 'latest developments in AI agents 2026'",
    expected_output="A list of 5 relevant sources with titles, URLs, and snippets",
    agent=search_agent,
)

crew = Crew(agents=[search_agent], tasks=[search_task], verbose=True)
result = crew.kickoff()
print("\n\n=== RESULT ===")
print(result)