def guard_app_install(app_id: str) -> dict:
    #app category
    return {"allowed": False, "rationale": "Age-inappropriate app", "action": "hard_lock"}