import lightgbm as lgb
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score

def train_lgbm(X, y, params=None):
    params = params or {
        "objective": "binary",
        "learning_rate": 0.05,
        "num_leaves": 64,
        "min_data_in_leaf": 30,
        "feature_fraction": 0.9
    }
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    models, oof = [], y.copy() * 0.0
    for tr, val in skf.split(X, y):
        dtr = lgb.Dataset(X.iloc[tr], label=y.iloc[tr])
        dvl = lgb.Dataset(X.iloc[val], label=y.iloc[val])
        m = lgb.train(params, dtr, num_boost_round=2000, valid_sets=[dvl],
                      callbacks=[lgb.early_stopping(100, verbose=False)])
        oof[val] = m.predict(X.iloc[val])
        models.append(m)
    return models, float(roc_auc_score(y, oof))