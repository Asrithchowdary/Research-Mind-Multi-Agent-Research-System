# 🔎 ResearchMind — Multi-Agent AI Research System

This project automates **end-to-end topic research** — searching the web, reading the most valuable source in depth, synthesizing a structured report, and critically evaluating that report's quality. It combines a multi-agent framework (CrewAI), a lightweight reasoning framework (LangChain), and a local LLM (Qwen2.5 via Ollama) to deliver a research pipeline where every citation is independently verified before it reaches the user.

---

## 🚀 Key Features

- 🔍 **Autonomous web search**: A tool-calling agent formulates queries and retrieves the top 5 relevant sources via the Tavily API
- 📖 **Intelligent source selection & scraping**: A second agent judges which source is most valuable and scrapes its full content
- ✍️ **Structured report synthesis**: An LLM chain writes a professional report (Introduction / Key Findings / Conclusion / Sources)
- 🧐 **Automated critique**: A second LLM chain scores the report and lists strengths and areas to improve
- 🛡️ **Citation guardrail**: Every source cited in the report is cross-checked against real search/scrape data — hallucinated citations are flagged before delivery
- 📊 **Evaluation suite**: Runs the full pipeline across multiple topics and tracks average quality score and citation-grounding rate over time
- 🌐 **FastAPI service**: Exposes the entire pipeline via a single callable endpoint.




## 💼 Technology Stack

| Tool/Library | Purpose |
|---|---|
| `crewai` | Multi-agent framework — powers the Search Agent and Reader Agent (ReAct-style tool-calling) |
| `langchain-core` | LCEL pipelines for the Writer and Critic chains |
| `langchain-ollama` | Connects LangChain chains to the local Ollama LLM |
| `tavily-python` | LLM-facing web search API client |
| `beautifulsoup4` | HTML parsing and text extraction for scraped pages |
| `requests` | HTTP requests for the scraper |
| `fastapi` / `uvicorn` | Exposes the pipeline as a callable HTTP service |
| `ollama` | Local LLM inference with Qwen2.5 |
| `python-dotenv` | Loads the Tavily API key from `.env` |

---

## 🔧 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/Asrithchowdary/ResearchMind.git
cd ResearchMind
```

### 2. Install uv (if not already installed)

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 3. Install dependencies

```bash
uv sync
```

### 4. Set up environment variables

Create a `.env` file in the root directory:

TAVILY_API_KEY=your-tavily-api-key


### 5. Install and run Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull qwen2.5:7b
```

---

## 🧠 Running the Project

▶️ **Start the API server**

```bash
uv run uvicorn src.research_mind_agent.main:app --reload
```

Then open `http://127.0.0.1:8000/docs` for the interactive Swagger UI.

▶️ **Run the evaluation suite**

```bash
uv run python run_eval.py
```

> 💡 You'll need Ollama installed and running locally with the `qwen2.5:7b` model.

---

## 🔌 LLM Setup (Ollama)

```bash
ollama pull qwen2.5:7b
ollama run qwen2.5:7b   # optional — test the model directly
```

Both the CrewAI agents and the LangChain chains send prompts to this local model — no data is sent to external LLM APIs.

**Note on provider routing:** CrewAI's `LLM` class must be pointed at Ollama's OpenAI-compatible endpoint explicitly:

```python
llm = LLM(
    model="openai_compatible/qwen2.5:7b",
    base_url="http://localhost:11434/v1",
    api_key="ollama",
)
```

---

## ✅ Sample Output

**API Request:**

```json
POST /research
{
  "topic": "latest developments in AI agents 2026"
}
```

**Report (excerpt):**
Research Report: Latest Developments in AI Agents for 2026
Key Findings
Market Maturity and Specialization
AI agents are becoming more specialized and less forgiving for
startups treating AI as an add-on rather than a core capability.
Increased Efficiency and Deployment Paradigms
New models enable local, continuous operation and low-latency
edge deployment, moving agents from experimental to essential
infrastructure.
AI Agents as Trusted Teammates
Agents are proliferating in daily work, with trust becoming a
central requirement as organizations rely on them for
decision-making.

**Citation Check:**

```json
{
  "total_cited": 5,
  "grounded_count": 5,
  "hallucinated_count": 0,
  "hallucinated_urls": [],
  "is_fully_grounded": true
}
```

**Critic Feedback:**

Score: 7/10
Strengths: Clear structure, relevant and timely sources, well-organized findings.
Areas to Improve: More in-depth analysis, additional supporting data,
clearer concluding statement.


---

## 📊 Evaluation Results

Run across 5 distinct research topics:
============================================================
EVAL SUMMARY

✓ latest developments in AI agents 2026 score=7/10 hallucinated=0
✓ impact of large language models on software eng... score=7/10 hallucinated=0
✓ current state of renewable energy adoption globa... score=8/10 hallucinated=0
✓ recent breakthroughs in quantum computing score=7/10 hallucinated=0
✓ trends in remote work post-2025 score=7/10 hallucinated=0

Average Critic Score: 7.2/10
Fully Grounded: 5/5
