import numpy as np

def heuristic_score(x: dict) -> float:
    s = 0.0
    s += np.clip((x["typos_per_100"] - 5) / 10.0, 0, 1) * 0.15
    s += np.clip((x["short_word_ratio"] - 0.4) / 0.4, 0, 1) * 0.10
    s += np.clip((x["path_erraticness"] - 0.45) / 0.4, 0, 1) * 0.20
    s += np.clip((x["emoji_ratio"] - 0.15) / 0.35, 0, 1) * 0.10
    s += np.clip((x["iki_mean"] - 140) / 120.0, 0, 1) * 0.10
    s += np.clip((x["swipe_speed_mean"] - 900) / 800.0, 0, 1) * 0.15
    s += np.clip((x["rtf_ms"] - 500) / 1000.0, 0, 1) * 0.20
    return float(np.clip(s, 0, 1))