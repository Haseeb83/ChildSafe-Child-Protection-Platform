export async function detectChild(payload, apiKey, baseUrl = "https://api.childsafe.dev/v1") {
    const res = await fetch(`${baseUrl}/v1/detect`, {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-API-Key": apiKey },
      body: JSON.stringify({ payload, context: { platform: "web" } })
    });
    if (!res.ok) throw new Error(await res.text());
    return await res.json();
  }
  
  export async function enforcePolicy(payload, apiKey, baseUrl = "https://api.childsafe.dev/v1") {
    const res = await fetch(`${baseUrl}/v1/enforce`, {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-API-Key": apiKey },
      body: JSON.stringify({ payload, context: { platform: "web" } })
    });
    if (!res.ok) throw new Error(await res.text());
    return await res.json();
  }
  
  // Example feature collection (placeholder)
  export function typingMetrics(events) {
    return {
      iki_mean: 180.0, iki_std: 95.0, typos_per_100: 9.0, backspace_rate: 0.1,
      avg_word_len: 3.8, short_word_ratio: 0.6, swipe_speed_mean: 1200.0,
      swipe_speed_std: 550.0, press_ms_mean: 140.0, press_ms_std: 60.0,
      path_erraticness: 0.65, emoji_ratio: 0.2, punct_ratio: 0.1,
      vocab_simplicity: 0.78, readability_fk: 2.5, rtf_ms: 900.0,
      dwell_std_ms: 420.0
    };
  }