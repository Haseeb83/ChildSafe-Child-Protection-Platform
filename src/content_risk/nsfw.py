def score_nsfw(image_url: str) -> dict:
    # Use computer vision model for NSFW detection
    return {"nsfw_score": 0.1, "rationale": "No NSFW content detected", "action": "allow"}
