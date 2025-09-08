import os
import sys
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

# Ensure project root is on sys.path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.rules.heuristics import heuristic_score
from src.data.schema import FEATURE_COLUMNS

# Load models from the project's artifacts folder
_repo_root = Path(__file__).resolve().parents[1]
candidate_paths = [
    _repo_root / "artifacts" / "lgbm_ensemble.joblib",
    _repo_root / "src" / "artifacts" / "lgbm_ensemble.joblib",
    _repo_root / "artifacts" / "models" / "lgbm_ensemble.joblib",
]

_model_path = next((p for p in candidate_paths if p.exists()), None)
if _model_path is None:
    MODELS = None
else:
    MODELS = joblib.load(str(_model_path))

def ml_score(row_df: pd.DataFrame) -> float:
    if MODELS is None:
        raise RuntimeError(
            "No models loaded. Ensure 'artifacts/lgbm_ensemble.joblib' exists and dependencies are installed."
        )

    # Ensure we pass the exact feature columns used during training in the same order
    missing = [c for c in FEATURE_COLUMNS if c not in row_df.columns]
    extra = [c for c in row_df.columns if c not in FEATURE_COLUMNS]
    if missing:
        raise RuntimeError(f"Missing feature columns required for prediction: {missing}")
    if extra:
        row_df = row_df.drop(columns=extra)

    X = row_df[FEATURE_COLUMNS]
    # Predict with each model and average
    return float(np.mean([m.predict(X)[0] for m in MODELS]))

def combined_score(x: dict) -> float:
    h = heuristic_score(x)
    m = ml_score(pd.DataFrame([x]))
    return 0.35 * h + 0.65 * m


if __name__ == "__main__":
    if _model_path is None:
        print("Model not found in candidate locations:")
        for p in candidate_paths:
            print(" -", p)
    else:
        print("Loaded models from:", _model_path)

    # If sample data is available, compute a combined score for the first row
    candidate_data_paths = [
        _repo_root / "artifacts" / "data.csv",
        _repo_root / "src" / "artifacts" / "data.csv",
    ]
    sample_csv = next((p for p in candidate_data_paths if p.exists()), None)
    if sample_csv is not None:
        df = pd.read_csv(sample_csv)
        row = df.iloc[0].to_dict()
        try:
            print("Combined score for first row:", combined_score(row))
        except Exception as e:
            print("Failed to compute combined score:", e)
    else:
        print("No sample data found in checked locations; run train.py to generate data.csv")