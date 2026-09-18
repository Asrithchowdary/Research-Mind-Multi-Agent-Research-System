import json
import re
from datetime import datetime
from src.research_mind_agent.crew import run_research_pipeline

with open("tests/eval_topics.json") as f:
    topics = json.load(f)

results = []

for case in topics:
    topic = case["topic"]
    print(f"\n{'='* 60}\nRunning: {topic}\n{'=' *60}")

    state = run_research_pipeline(topic)
    score_match = re.search(r"Score:\s*(\d+)/10", state["feedback"])
    score = int(score_match.group(1)) if score_match else None
    results.append({
        "topic": topic,
        "score": score,
        "is_fully_grounded": state["citation_check"]["is_fully_grounded"],
        "hallucinated_count": state["citation_check"]["hallucinated_count"],
    })

print(f"\n\n{'='*60}")
print("EVAL SUMMARY")
print(f"{'='*60}")

valid_scores = [r["score"] for r in results if r["score"] is not None]
avg_score = sum(valid_scores) / len(valid_scores) if valid_scores else 0
grounded_count = sum(1 for r in results if r["is_fully_grounded"])

for r in results:
    status = "✓" if r.get("is_fully_grounded") else "✗"
    print(f"{status} {r['topic'][:50]:50} score={r.get('score')}/10  hallucinated={r.get('hallucinated_count', 'N/A')}")
    
print(f"\nAverage Critic Score: {avg_score:.1f}/10")
print(f"Fully Grounded: {grounded_count}/{len(results)}")

#Log run for tracking over time

log_entry ={
    "timestamp": datetime.now().isoformat(),
    "avg_score": avg_score,
    "grounded_rate": grounded_count / len(results),
    "results": results,
}
with open("tests/eval_history.jsonl", "a") as f:
    f.write(json.dumps(log_entry) + "\n")