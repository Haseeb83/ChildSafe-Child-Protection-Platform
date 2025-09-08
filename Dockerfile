FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "80", "--ssl-keyfile", "/certs/key.pem", "--ssl-certfile", "/certs/cert.pem"]  # HTTPS in prod
# Volumes for certs: -v /path/to/certs:/certs