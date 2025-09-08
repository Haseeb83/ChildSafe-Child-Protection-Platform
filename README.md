# ChildSafe: Child Protection Platform

## Overview
**ChildSafe** is a privacy-first, production-ready platform designed to detect child users in apps, games, and web platforms, delivering a **Child Likelihood Score (CLS)** (0–1) and enforcing kid-safe policies. It is compliant with **COPPA**, **GDPR-K**, **UK AADC**, and **India DPDP** by using behavioral signals without PII or biometrics. The platform supports web (JavaScript) and Android (Kotlin) SDKs, a scalable **FastAPI** backend, and is deployable as a standalone API for integration via Postman or mobile apps.

- **Milestone 1**: Delivered a Persona Verification Engine using synthetic data, rule-based heuristics (HCLS), and a LightGBM model (ROC-AUC ≥ 0.90, precision ≥ 0.90, recall ≥ 0.75, false positives ≤ 5%, latency ≤ 40ms, model < 50MB).
- **Milestone 2**: Added a secure FastAPI backend with endpoints (`/v1/detect`, `/v1/enforce`, `/v1/telemetry/batch`, `/v1/feedback`, `/v1/health`, `/v1/quota`), SDKs, Dockerized deployment, and content risk modules (stubs for grooming, NSFW, etc.).

## Features
- **CLS Engine**: Hybrid rule-based (HCLS) and ML (LightGBM) model for child detection, supporting edge cases (slow-typing adults, neurodiversity, non-native speakers, accessibility keyboards).
- **Modality Coverage**: Handles low-typing scenarios via hooks for voice, video, app focus, and mic usage signals.
- **Content Risk**: Stubs for grooming/toxicity scoring, image NSFW checks, link reputation, live-chat risk, screen-time limits, app-install/purchase guardrails, and location-sharing restrictions.
- **API Endpoints**: Secure, rate-limited endpoints with OAuth2/JWT authentication, returning `cls`, `confidence`, `reasons[]`, `action`, `feature_flags`, `limits`, and `policy_version`.
- **Policy Engine**: Server-side rules (`policy.yaml`) for time-of-day, geofence, URL/app categories, age bands, and prior violations, mapping to actions (`allow`, `soft_lock`, `hard_lock`, `PIN_challenge`, `notify_guardian`).
- **Security**: HTTPS, OAuth2/JWT with key rotation, rate limiting, audit logs, and basic RBAC (user/admin roles).
- **Privacy**: No PII/biometrics; 30-day log retention; anonymization and deletion via `/v1/feedback`.
- **Deployment**: Dockerized for Google Cloud Run, Render, Railway, or Hugging Face Spaces, with HTTPS enforced.
- **SDKs**: Web (JavaScript) and Android (Kotlin) for seamless integration.

## Project Structure
```
childsafe/
├── README.md
├── requirements.txt
├── .env.example
├── Dockerfile
├── docker-compose.yml
├── policy.yaml
├── openapi.yaml
├── src/
│   ├── data/
│   │   ├── synth_generator.py
│   │   └── schema.py
│   ├── features/
│   │   ├── typing.py
│   │   ├── touch.py
│   │   ├── language.py
│   │   ├── response_time.py
│   │   └── extra.py
│   ├── rules/
│   │   └── heuristics.py
│   ├── models/
│   │   ├── mlp_torch.py
│   │   ├── lgbm.py
│   │   └── calibrate.py
│   ├── content_risk/
│   │   ├── toxicity.py
│   │   ├── nsfw.py
│   │   ├── link_reputation.py
│   │   ├── live_chat.py
│   │   ├── screen_time.py
│   │   ├── app_install.py
│   │   └── location.py
│   ├── api/
│   │   ├── main.py
│   │   ├── security.py
│   │   └── audit.py
│   ├── train.py
│   ├── evaluate.py
│   ├── infer.py
│   ├── export.py
├── notebooks/
│   └── eda.ipynb
├── artifacts/
│   ├── synth_train.csv
│   ├── lgbm_ensemble.joblib
│   ├── report.json
│   ├── confusion.png
│   ├── config.yaml
│   └── audit.log
├── sdk/
│   ├── web.js
│   └── android/
│       └── ChildSafe.kt
├── tests/
│   ├── test_api.py
│   └── load.js
├── docs/
│   └── ChildSafe.postman_collection.json
├── .github/
    └── workflows/
        └── ci.yml
```

## Setup
1. **Clone Repository**:
   ```bash
   git clone <repo-url>
   cd childsafe
   ```

2. **Set Up Environment**:
   ```bash
   python -m venv venv
   # Windows: venv\Scripts\activate
   # macOS/Linux: source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Generate Secrets**:
   ```bash
   openssl rand -hex 32  # For SECRET_KEY
   ```
   Copy `.env.example` to `.env` and fill in:
   ```
   SECRET_KEY=your_jwt_secret_here
   API_KEY_DB=sqlite:///api_keys.db
   AUDIT_LOG_PATH=artifacts/audit.log
   RATE_LIMIT=1000/minute
   ```

4. **Train Model**:
   ```bash
   python src/train.py
   ```
   Outputs: `artifacts/synth_train.csv`, `artifacts/lgbm_ensemble.joblib`, `artifacts/report.json`, `artifacts/confusion.png`.

5. **Run API Locally**:
   ```bash
   uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
   ```
   Test at `https://localhost:8000/docs` (use self-signed certs locally or disable SSL for testing).

## Endpoint/Features
| Endpoint | Method | Request Fields | Response Schema | /v1/enforce Actions |
|----------|--------|----------------|-----------------|---------------------|
| `/v1/detect` | POST | `payload`: {17 features, e.g., `iki_mean: 180.0`}<br>`extra_signals`: {voice_events, video_events, focus_events, mic_events}<br>`context`: {platform, locale} | `cls`: Float (0–1)<br>`confidence`: Float (0–1)<br>`reasons`: List[str] (e.g., ["High typing irregularity"])<br>`threshold`: Float (default 0.5) | N/A |
| `/v1/enforce` | POST | As `/v1/detect` +<br>`content_risk`: {text, image_url, url, chat_text, session_duration, app_id, sharing} | `cls`, `confidence`, `reasons[]`, `threshold`,<br>`action`: String (`allow`, `soft_lock`, `hard_lock`, `PIN_challenge`, `notify_guardian`)<br>`feature_flags`: Dict (e.g., `restrict_chat: true`, `block_iap: true`, `safe_recommendations: true`, `blur_adult_images: true`, `disable_age_inappropriate_modes: ["PVP_MATURE", "NSFW_CHAT"]`, `report_button_visible: true`, `ui_mode: "kid"`)<br>`limits`: Dict (e.g., `playtime_min: 30`)<br>`policy_version`: String (e.g., `rules-2025.09.1`) | `allow`, `soft_lock`, `hard_lock`, `PIN_challenge`, `notify_guardian` |
| `/v1/telemetry/batch` | POST | `telemetry`: [{event}] | `status`: String (e.g., "received") | N/A |
| `/v1/feedback` | POST | `feedback`: {str} | `status`: String (e.g., "feedback received") | N/A |
| `/v1/health` | GET | None | `status`: String<br>`uptime_sec`: Int<br>`model_version`: String | N/A |
| `/v1/quota` | GET | None | `tier`: String<br>`monthly_limit`: Int<br>`remaining`: Int<br>`reset_at`: String | N/A |

## Deployment
### Local (Docker)
```bash
docker build -t childsafe .
# Generate self-signed certs for local testing
openssl req -x509 -newkey rsa:4096 -nodes -out certs/cert.pem -keyout certs/key.pem -days 365
docker run -p 8000:80 -v $(pwd)/certs:/certs -e SECRET_KEY=your_jwt_secret -e RATE_LIMIT=1000/minute childsafe
```
Test at `https://localhost:8000/docs`.

### Google Cloud Run
docker build -t gcr.io/[PROJECT-ID]/childsafe:latest .
gcloud auth configure-docker
docker push gcr.io/[PROJECT-ID]/childsafe:latest
gcloud run deploy childsafe \
  --image gcr.io/[PROJECT-ID]/childsafe:latest \
  --platform managed \
  --region us-central1 \
  --set-env-vars "SECRET_KEY=your_jwt_secret,RATE_LIMIT=1000/minute" \
  --allow-unauthenticated
Get the service URL (e.g., `https://childsafe-xxx.a.run.app`).

### Render
1. Push repo to GitHub.
2. In Render: New > Web Service > Docker > Connect GitHub repo.
3. Set `PORT=80`, add env vars from `.env.example` (`SECRET_KEY`, etc.).
4. Enable auto-deploy; Render provides HTTPS.

### Railway
1. Push to GitHub.
2. In Railway: New Project > Deploy from GitHub > Select repo.
3. Configure `PORT=80`, add env vars from `.env.example`.
4. Railway provides HTTPS by default.

### Hugging Face Spaces
1. Create a Space, select Docker template.
2. Upload repo or sync with GitHub.
3. In Settings, set `PORT=80`, add secrets (`SECRET_KEY`, etc.).
4. Note: Limited scalability; suitable for demos.

## Security
- **HTTPS**: Enforced via `--ssl-keyfile` and `--ssl-certfile` in `Dockerfile`; use Let’s Encrypt in production.
- **Authentication**: OAuth2/JWT with key rotation (`src/api/security.py`); obtain token via `/token`.
  curl -X POST "https://api.childsafe.dev/token" -d "username=user&password=pass" -H "Content-Type: application/x-www-form-urlencoded"
  ```
- **Rate Limiting**: Configured via `RATE_LIMIT` env (e.g., `1000/minute`) using `slowapi`.
- **Audit Logs**: Saved to `artifacts/audit.log` (`src/api/audit.py`).
- **RBAC**: Roles (`user`, `admin`); `/v1/telemetry/batch` requires `admin`.
- **Secrets**: Store in `.env` (copy `.env.example`); inject via Docker or Cloud Run env vars.

## Privacy
- **PII Minimization**: Only behavioral aggregates (e.g., `iki_mean`) processed; no raw events stored.
- **Retention**: Audit logs retained for 30 days; delete via `/v1/feedback` or admin API.
- **Anonymization**: Tokens/IPs hashed in logs.
- **COPPA Compliance**: No persistent profiles; parental consent hook via `notify_guardian`.

## SDK Integration
- **Web (JavaScript)**:
  ```javascript
  import { detectChild, enforcePolicy } from './src/sdk/web.js';
  const payload = {...}; // From events
  const res = await detectChild(payload, 'jwt_token', 'https://api.childsafe.dev');
  if (res.decision === 'child') {
    const policy = await enforcePolicy(payload, 'jwt_token');
    applyPolicy(policy.policy); // Restrict features
  }
  ```
- **Android (Kotlin)**:
  ```kotlin
  val payload = ChildSafe.captureMetrics(events)
  val res = ChildSafe.detect(payload, "jwt_token", "https://api.childsafe.dev")
  if (res.getString("decision") == "child") {
      val policy = ChildSafe.enforce(payload, "jwt_token")
      // Apply policy
  }
  ```

## Testing
- **Postman**: Import `docs/ChildSafe.postman_collection.json`; set `base_url` to `https://api.childsafe.dev` and use JWT flow.

## Deliverables
- **Core API**: Endpoints (`/v1/detect`, `/v1/enforce`, `/v1/telemetry/batch`, `/v1/feedback`, `/v1/health`, `/v1/quota`) with OpenAPI (`openapi.yaml`) and Postman collection.
- **Policy Engine**: `policy.yaml` with rules for time-of-day, geofence, categories, age bands, violations.
- **Modality Coverage**: Hooks in `src/features/extra.py` for voice/video/focus/mic signals.
- **Content Risk**: Stubs in `src/content_risk/` for toxicity, NSFW, links, chat, screen-time, app-install, location.
- **Security**: HTTPS, OAuth2/JWT, rate limiting, audit logs, RBAC.
- **Deployment**: Dockerfile, Cloud Run steps, Render/Railway/HF Spaces guides.
- **Privacy**: Data-flow diagram, no PII, 30-day retention, delete/anonymize via `/v1/feedback`.

