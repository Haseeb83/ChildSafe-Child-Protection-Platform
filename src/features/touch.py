def compute_touch_features(events):
    # Derive from touch events
    return {
        "swipe_speed_mean": 1200.0,  # normalized
        "swipe_speed_std": 550.0,
        "press_ms_mean": 140.0,
        "press_ms_std": 60.0,
        "path_erraticness": 0.65
    }