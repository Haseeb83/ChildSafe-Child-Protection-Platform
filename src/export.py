import joblib
import torch
from src.models.mlp_torch import MLP
from src.data.schema import FEATURE_COLUMNS

def export_lgbm(models, path="artifacts/lgbm_ensemble.joblib"):
    joblib.dump(models, path)

def export_torch(model, example_input, path="artifacts/mlp.pt"):
    traced = torch.jit.trace(model, example_input)
    traced.save(path)

if __name__ == "__main__":
    models = joblib.load("artifacts/lgbm_ensemble.joblib")
    export_lgbm(models)
    mlp = MLP(len(FEATURE_COLUMNS))
    example_input = torch.randn(1, len(FEATURE_COLUMNS))
    export_torch(mlp, example_input)