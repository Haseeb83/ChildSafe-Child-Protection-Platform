import logging
import os

AUDIT_LOG_PATH = os.getenv("AUDIT_LOG_PATH", "artifacts/audit.log")

logging.basicConfig(filename=AUDIT_LOG_PATH, level=logging.INFO, format="%(asctime)s - %(message)s")

def log_audit(key: str, endpoint: str, request: dict, response: dict):
    logging.info(f"Key: {key}, Endpoint: {endpoint}, Request: {request}, Decision: {response['cls']}, Policy: {response.get('policy_version', 'N/A')}")