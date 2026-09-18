import re
from crewai import Task, Crew

from .agents import search_agent, reader_agent
from .chains import writer_chain, critic_chain


def extract_urls(text: str) -> set:
    """Pulls all http(s) URLs out of a block of text."""
    return set(re.findall(r"https?://[^\s\)\]\"']+", text))


def validate_citations(report: str, search_result: str, scraped_content: str) -> dict:
    """
    Guardrail: checks that every URL cited in the report's Sources section
    actually appeared in the real search results or scraped content.
    """
    cited_urls = extract_urls(report)
    real_urls = extract_urls(search_result) | extract_urls(scraped_content)

    hallucinated = cited_urls - real_urls
    grounded = cited_urls & real_urls

    return {
        "total_cited": len(cited_urls),
        "grounded_count": len(grounded),
        "hallucinated_count": len(hallucinated),
        "hallucinated_urls": list(hallucinated),
        "is_fully_grounded": len(hallucinated) == 0,
    }


def run_research_pipeline(topic: str) -> dict:
    state = {
        "search_result": "",
        "scraped_content": "",
        "report": "",
        "feedback": "",
        "citation_check": None,
    }

    #Step 1- Search Agent(CrewAI)
    search_task = Task(
        description=f"Search for information about '{topic}'",
        expected_output="A list of 5 relevant sources with titles, URLs, and snippets",
        agent=search_agent,
    )
    search_crew = Crew(agents=[search_agent], tasks=[search_task], verbose=True)
    state["search_result"] = str(search_crew.kickoff())

    #Step 2- Reader Agent (Crew AI) - picks and scrapes the most promising source
    read_task = Task(
        description=(
            f"From these search results, identify the single most promising URL "
            f"and scrape its full content:\n\n{state['search_result']}"
        ),
        expected_output="The full scraped text content of the most relevant source",
        agent=reader_agent,
    )
    read_crew = Crew(agents=[reader_agent], tasks=[read_task], verbose=True)
    state["scraped_content"] = str(read_crew.kickoff())

    #Step 3- Writer Chain(Langchain) - pure synthesis, no tools
    state["report"] = writer_chain.invoke({
        "search_results": state["search_result"],
        "scraped_content": state["scraped_content"],
    })

    # Guardrail — runs BEFORE the critic sees it
    state["citation_check"] = validate_citations(
        state["report"], state["search_result"], state["scraped_content"]
    )
    if not state["citation_check"]["is_fully_grounded"]:
        state["report"] += (
            f"\n\n⚠️ GUARDRAIL WARNING: {state['citation_check']['hallucinated_count']} "
            f"cited source(s) could not be verified against actual search/scrape data: "
            f"{state['citation_check']['hallucinated_urls']}"
        )

    #Step 4- Critic chain(Langchain)- pure evaluation, no tools
    state["feedback"] = critic_chain.invoke({"report": state["report"]})

    return state