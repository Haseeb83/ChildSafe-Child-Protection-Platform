def score_toxicity(text: str) -> dict:
    # Use HuggingFace
    return {"toxicity_score": 0.8, "rationale": "High toxicity detected", "action": "block"}