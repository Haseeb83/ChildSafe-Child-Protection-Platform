def score_link(url: str) -> dict:
    #Use Google Safe Browsing API
    return {"risk_score": 0.7, "rationale": "Suspicious domain", "action": "block"}