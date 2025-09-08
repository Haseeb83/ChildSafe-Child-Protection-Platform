def guard_location(sharing: bool) -> dict:
    # Based on CLS
    return {"allowed": not sharing, "rationale": "Location sharing disabled for child", "action": "block"}