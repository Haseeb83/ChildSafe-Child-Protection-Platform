# ChildSafe-Child-Protection-Platform
ChildSafe is a privacy-first, production-ready AI platform designed to detect child users in apps, games, and websites and enforce kid-safe policies. It delivers a Child Likelihood Score (CLS) (0–1) and ensures compliance with COPPA, GDPR-K, UK AADC, and India DPDP, all without storing PII or biometrics.

# 🔑 Key Highlights

Detection Engine: Hybrid rule-based + ML (LightGBM) model with ROC-AUC ≥ 0.90 and low latency (<40ms).

FastAPI Backend: Secure endpoints (/v1/detect, /v1/enforce, /v1/telemetry/batch, /v1/feedback, /v1/health, /v1/quota) with OAuth2/JWT authentication.

Policy Enforcement: Rules for geofencing, time-of-day, age bands, violations → actions (allow, lock, PIN challenge, notify guardian).

Content Safety: Modules for grooming, toxicity, NSFW images, risky links, live-chat moderation, screen-time limits, and purchase guardrails.

Privacy & Security: No PII/biometrics, 30-day anonymized logs, HTTPS, RBAC, rate limiting, and audit logs.

SDKs: Web (JavaScript) + Android (Kotlin) for seamless integration into apps and games.

Deployment Ready: Dockerized for Google Cloud Run, Render, Railway, Hugging Face Spaces.

# 🚀 Tech Stack

Backend: FastAPI, Docker, OAuth2/JWT

ML Models: LightGBM, PyTorch MLP, Rule-based heuristics

Deployment: Google Cloud Run, Render, Railway, Hugging Face Spaces

SDKs: Web (JavaScript) & Android (Kotlin)

# ✅ Use Cases

Detect underage users in apps, games, and websites

Enforce age-appropriate policies automatically

Prevent exposure to unsafe content & risky interactions

Comply with global child data protection regulations
