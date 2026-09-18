from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOllama(model="qwen2.5:7b")

WRITER_PROMPT = ChatPromptTemplate.from_template(
    """You are an expert research writer. Using the search results and scraped
content below, write a professional research report with this exact structure:
Introduction
Key Findings (at least 3 well-explained points)
Conclusion
Sources (list all URLs referenced)

Search Results:
{search_results}

Scraped Content:
{scraped_content}
"""
)

writer_chain = WRITER_PROMPT | llm | StrOutputParser()

CRITIC_PROMPT = ChatPromptTemplate.from_template(
    """You are a critical reviewer. Evaluate the following research report
objectively. Respond in exactly this format:
    
Score: X/10
Strengths: (bulleted list)
Areas to Improve: (bulleted list)
One-line Verdict: (a single summary sentence)

Report:
{report}
"""
)

critic_chain = CRITIC_PROMPT | llm | StrOutputParser()

if __name__ == "__main__":
    sample_search = "Title: Test Article\nURL: https://example.com\nSnippet: AI agents are evolving rapidly in 2026."
    sample_scraped = "AI agents are increasingle autonomous, with tool-calling and multi-step reasoning becoming standard."

    report = writer_chain.invoke({
        "search_results": sample_search,
        "scraped_content": sample_scraped,
    })
    print("=== REPORT ====")
    print(report)

    feedback = critic_chain.invoke({"report": report})
    print("\n=== FEEDBACK ===")
    print(feedback)