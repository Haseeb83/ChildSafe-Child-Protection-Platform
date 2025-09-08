import torch
import torch.nn as nn

class MLP(nn.Module):
    def __init__(self, in_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_dim, 128), nn.ReLU(), nn.Dropout(0.15),
            nn.Linear(128, 64), nn.ReLU(), nn.Dropout(0.10),
            nn.Linear(64, 1)
        )
    def forward(self, x): return self.net(x).squeeze(-1)

def predict_proba(model, X_t):
    with torch.no_grad():
        logits = model(torch.as_tensor(X_t.values, dtype=torch.float32))
        return torch.sigmoid(logits).numpy()