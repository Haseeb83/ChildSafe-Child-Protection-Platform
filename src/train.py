import os
import sys
from pathlib import Path

import pandas as pd
import joblib
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.data.synth_generator import generate
from src.models.lgbm import train_lgbm
from src.evaluate import evaluate_and_report

if __name__ == "__main__":
    df = generate()
    # Ensure artifacts directory exists before saving data and outputs
    os.makedirs("artifacts", exist_ok=True)

    # Persist generated dataset for inspection / reproducibility
    df.to_csv(os.path.join("artifacts", "data.csv"), index=False)

    X, y = df.drop(columns=["is_child"]), df["is_child"]
    models, auc = train_lgbm(X, y)
    # Ensure artifacts directory exists before writing outputs
    os.makedirs("artifacts", exist_ok=True)

    joblib.dump(models, "artifacts/lgbm_ensemble.joblib")
    evaluate_and_report(models, X, y, "artifacts/report.json", "artifacts/confusion.png")