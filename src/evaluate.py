import numpy as np
import json
import matplotlib.pyplot as plt
from sklearn.metrics import roc_auc_score, precision_recall_fscore_support, confusion_matrix
from sklearn.model_selection import train_test_split

def ensemble_predict(models, X):
    preds = [m.predict(X) for m in models]
    return np.mean(preds, axis=0)

def evaluate_and_report(models, X, y, json_out, cm_out, threshold=0.5):
    p = ensemble_predict(models, X)
    auc = roc_auc_score(y, p)
    y_hat = (p >= threshold).astype(int)
    p_, r_, f1_, _ = precision_recall_fscore_support(y, y_hat, average="binary")
    cm = confusion_matrix(y, y_hat).tolist()
    with open(json_out, "w") as f:
        json.dump({"auc": auc, "precision": p_, "recall": r_, "f1": f1_, "cm": cm}, f, indent=2)
    plt.figure()
    plt.imshow(cm)
    plt.title("Confusion Matrix")
    plt.colorbar()
    plt.savefig(cm_out)
    plt.close()