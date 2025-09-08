def compute_voice_features(events):
    # Placeholder: Derive from voice input (e.g., speech rate, pitch variance for child-like voice)
    return {
        "speech_rate_wpm": 120.0,  # Words per minute (children slower)
        "pitch_variance": 0.6  # Higher variance for kids
    }

def compute_video_features(events):
    # Placeholder: Derive from video consumption (e.g., watch time, skip rate)
    return {
        "video_watch_ratio": 0.8,  # Fraction watched (kids may skip less)
        "skip_rate": 0.3  # High skips → adult
    }

def compute_focus_features(events):
    # Placeholder: App focus changes (e.g., switch frequency)
    return {
        "app_switch_freq": 5.0  # Switches per minute (kids higher)
    }

def compute_mic_features(events):
    # Placeholder: Mic usage events (e.g., duration, background noise)
    return {
        "mic_duration_sec": 30.0,  # Short bursts → child play
        "noise_level": 0.7  # Higher noise → kids
    }

def aggregate_extra_signals(voice_events, video_events, focus_events, mic_events):
    features = {}
    features.update(compute_voice_features(voice_events))
    features.update(compute_video_features(video_events))
    features.update(compute_focus_features(focus_events))
    features.update(compute_mic_features(mic_events))
    return features