from fastapi import FastAPI
from pydantic import BaseModel

from .crew import run_research_pipeline

app = FastAPI(title="ResearchMind -Multi-Agent Research System")

class ResearchRequest(BaseModel):
    topic: str

@app.post("/research")
def research(request: ResearchRequest):
    """Runs the full Search-> Read -> Write -> Critique pipeline for a topic."""
    result = run_research_pipeline(request.topic)
    return {
        "topic": request.topic,
        "report": result["report"],
        "feedback": result["feedback"],
        "citation_check": result["citation_check"],
    }

@app.get("/")
def root():
    return {"status": "ResearchMind is running"}