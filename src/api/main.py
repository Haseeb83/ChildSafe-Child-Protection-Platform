from fastapi import FastAPI, Depends, HTTPException, Response, Request
from pydantic import BaseModel, Field
from typing import Dict, Optional, List
import time
import json
import os
import yaml
from datetime import datetime
from src.infer import combined_score
from src.data.schema import FEATURE_COLUMNS
from src.api.security import oauth2_scheme, get_current_user, rbac, limiter, create_jwt
from src.api.audit import log_audit
from src.content_risk.toxicity import score_toxicity
from src.content_risk.link_reputation import score_link
from src.content_risk.live_chat import score_live_chat
from src.content_risk.screen_time import enforce_screen_time
from src.content_risk.app_install import guard_app_install
from src.content_risk.location import guard_location
from src.content_risk.nsfw import score_nsfw
from src.features.extra import aggregate_extra_signals
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

app = FastAPI(title="ChildSafe.API", version="1.0")
app.state.limiter = limiter
@app.on_event("startup")
async def startup():
    # Load policy
    with open("policy.yaml", "r") as f:
        app.state.policy = yaml.safe_load(f)

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    role = "user"  # "admin" based on auth
    return {"access_token": create_jwt(role), "token_type": "bearer"}

class DetectRequest(BaseModel):
    payload: Dict[str, float] = Field(..., description="Feature map")
    extra_signals: Optional[Dict] = None  #For modality coverage
    context: Optional[Dict[str, str]] = None

class EnforceRequest(DetectRequest):
    content_risk: Optional[Dict] = None  # For content risk 

class DetectResponse(BaseModel):
    cls: float
    confidence: float = 1.0  # uncertainty 
    reasons: List[str]
    threshold: float = 0.5

class EnforceResponse(DetectResponse):
    action: str  # allow/soft_lock/hard_lock/PIN_challenge/notify_guardian
    feature_flags: Dict[str, bool]
    limits: Dict[str, int]
    policy_version: str

@app.post("/v1/detect", response_model=DetectResponse)
@limiter.limit(os.getenv("RATE_LIMIT", "1000/minute"))
def detect(request: Request, req: DetectRequest, token: str = Depends(oauth2_scheme)):
    _ = get_current_user(token)
    payload = {k: float(req.payload[k]) for k in FEATURE_COLUMNS}
    if req.extra_signals:
        payload.update(aggregate_extra_signals(**req.extra_signals))
    score = combined_score(payload)
    reasons = ["High typing irregularity", "Erratic touch patterns"]  # Stub from SHAP or rules
    response = DetectResponse(cls=score, confidence=1.0 - (score - 0.5)**2, reasons=reasons)
    log_audit(token, "/v1/detect", req.dict(), response.dict())
    return response

@app.post("/v1/enforce", response_model=EnforceResponse)
@limiter.limit(os.getenv("RATE_LIMIT", "1000/minute"))
def enforce(request: Request, req: EnforceRequest, token: str = Depends(oauth2_scheme)):
    _ = get_current_user(token)
    payload = {k: float(req.payload[k]) for k in FEATURE_COLUMNS}
    if req.extra_signals:
        payload.update(aggregate_extra_signals(**req.extra_signals))
    score = combined_score(payload)
    policy = app.state.policy
    action = "allow"
    feature_flags = {}
    limits = {}
    reasons = []
    # Apply policies
    current_time = datetime.now().time()
    if policy["bedtime_window"]["start"] < current_time < policy["bedtime_window"]["end"]:
        action = "soft_lock"
        reasons.append("Bedtime policy")
    if req.content_risk:
        risk_scores = {
            "toxicity": score_toxicity(req.content_risk.get("text", "")),
            "nsfw": score_nsfw(req.content_risk.get("image_url", "")),
            "link": score_link(req.content_risk.get("url", "")),
            "live_chat": score_live_chat(req.content_risk.get("chat_text", "")),
            "screen_time": enforce_screen_time(req.content_risk.get("session_duration", 0)),
            "app_install": guard_app_install(req.content_risk.get("app_id", "")),
            "location": guard_location(req.content_risk.get("sharing", False))
        }
        for risk, result in risk_scores.items():
            if result["action"] != "allow":
                action = max(action, result["action"], key=lambda a: ["allow", "soft_lock", "hard_lock", "PIN_challenge", "notify_guardian"].index(a))
                reasons.append(result["rationale"])
    response = EnforceResponse(cls=score, confidence=1.0 - (score - 0.5)**2, reasons=reasons, action=action, feature_flags=feature_flags, limits=limits, policy_version=policy["version"])
    log_audit(token, "/v1/enforce", req.dict(), response.dict())
    return response

@app.post("/v1/telemetry/batch")
@limiter.limit("100/minute")
def telemetry_batch(request: Request, req: Dict, token: str = Depends(oauth2_scheme)):
    role = get_current_user(token)
    if role != "admin":
        raise HTTPException(403, "Admin only")
    # Stub: Process batch telemetry for federated updates
    return {"status": "received"}

@app.post("/v1/feedback")
@limiter.limit("10/minute")
def feedback(request: Request, req: Dict, token: str = Depends(oauth2_scheme)):
    _ = get_current_user(token)
    # Stub: Log misclassification feedback
    with open("artifacts/feedback.log", "a") as f:
        f.write(json.dumps(req) + "\n")
    return {"status": "feedback received"}

@app.get("/v1/health")
def health():
    return {"status": "ok", "uptime_sec": int(time.time()), "model_version": "cs-ml-2025.08.1"}

@app.get("/v1/quota")
def quota(token: str = Depends(oauth2_scheme)):
    _ = get_current_user(token)
    return {"tier": "Pro", "monthly_limit": 500000, "remaining": 471233, "reset_at": "2025-10-01T00:00:00Z"}