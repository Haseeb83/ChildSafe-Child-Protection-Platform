def enforce_screen_time(session_duration: float) -> dict:
    # Based on limits
    return {"exceeded": session_duration > 1200, "action": "soft_lock"}