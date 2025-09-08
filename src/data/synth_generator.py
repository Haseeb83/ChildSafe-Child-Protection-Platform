import numpy as np
import pandas as pd
from .schema import FEATURE_COLUMNS, TARGET

def _child_dist(n):
    return {
        "iki_mean": np.random.normal(180, 40, n),
        "iki_std": np.random.normal(95, 20, n),
        "typos_per_100": np.random.normal(9, 3, n),
        "backspace_rate": np.random.beta(2, 7, n),
        "avg_word_len": np.random.normal(3.8, 0.5, n),
        "short_word_ratio": np.random.beta(6, 2, n),
        "swipe_speed_mean": np.random.normal(1200, 250, n),
        "swipe_speed_std": np.random.normal(550, 120, n),
        "press_ms_mean": np.random.normal(140, 35, n),
        "press_ms_std": np.random.normal(60, 15, n),
        "path_erraticness": np.random.normal(0.65, 0.12, n),
        "emoji_ratio": np.random.beta(4, 7, n),
        "punct_ratio": np.random.beta(3, 9, n),
        "vocab_simplicity": np.random.normal(0.78, 0.07, n),
        "readability_fk": np.random.normal(2.5, 0.8, n),
        "rtf_ms": np.random.normal(900, 200, n),
        "dwell_std_ms": np.random.normal(420, 110, n),
    }

def _adult_dist(n):
    return {
        "iki_mean": np.random.normal(130, 25, n),
        "iki_std": np.random.normal(55, 15, n),
        "typos_per_100": np.random.normal(3, 1.5, n),
        "backspace_rate": np.random.beta(2, 12, n),
        "avg_word_len": np.random.normal(5.2, 0.4, n),
        "short_word_ratio": np.random.beta(2, 6, n),
        "swipe_speed_mean": np.random.normal(800, 180, n),
        "swipe_speed_std": np.random.normal(240, 80, n),
        "press_ms_mean": np.random.normal(90, 20, n),
        "press_ms_std": np.random.normal(30, 10, n),
        "path_erraticness": np.random.normal(0.32, 0.08, n),
        "emoji_ratio": np.random.beta(2, 12, n),
        "punct_ratio": np.random.beta(7, 6, n),
        "vocab_simplicity": np.random.normal(0.52, 0.06, n),
        "readability_fk": np.random.normal(7.8, 1.2, n),
        "rtf_ms": np.random.normal(350, 120, n),
        "dwell_std_ms": np.random.normal(180, 60, n),
    }

def generate(n_child=5000, n_adult=5000, seed=42):
    rng = np.random.default_rng(seed)
    child = pd.DataFrame(_child_dist(n_child))
    child[TARGET] = 1
    adult = pd.DataFrame(_adult_dist(n_adult))
    adult[TARGET] = 0
    df = pd.concat([child, adult], ignore_index=True)
    df = df.sample(frac=1, random_state=seed).reset_index(drop=True)
    return df[FEATURE_COLUMNS + [TARGET]]