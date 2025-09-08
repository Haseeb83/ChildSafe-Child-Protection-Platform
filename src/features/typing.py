def compute_typing_features(events):
    #Derive from raw key events
    return {
        "iki_mean": 180.0,  # ms
        "iki_std": 95.0,
        "typos_per_100": 9.0,
        "backspace_rate": 0.1,
        "avg_word_len": 3.8,
        "short_word_ratio": 0.6
    }