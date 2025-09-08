package com.childsafe.sdk

import org.json.JSONObject
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

object ChildSafe {
    data class Payload(val map: Map<String, Double>)

    private val client = OkHttpClient()

    suspend fun detect(payload: Payload, apiKey: String, baseUrl: String = "https://api.childsafe.dev/v1"): JSONObject = withContext(Dispatchers.IO) {
        val body = JSONObject(mapOf("payload" to payload.map, "context" to mapOf("platform" to "android")))
        val request = Request.Builder()
            .url("$baseUrl/v1/detect")
            .post(body.toString().toRequestBody("application/json".toMediaType()))
            .header("X-API-Key", apiKey)
            .build()
        val response = client.newCall(request).execute()
        if (!response.isSuccessful) throw Exception(response.body?.string() ?: "Request failed")
        JSONObject(response.body?.string() ?: "{}")
    }

    suspend fun enforce(payload: Payload, apiKey: String, baseUrl: String = "https://api.childsafe.dev/v1"): JSONObject = withContext(Dispatchers.IO) {
        val body = JSONObject(mapOf("payload" to payload.map, "context" to mapOf("platform" to "android")))
        val request = Request.Builder()
            .url("$baseUrl/v1/enforce")
            .post(body.toString().toRequestBody("application/json".toMediaType()))
            .header("X-API-Key", apiKey)
            .build()
        val response = client.newCall(request).execute()
        if (!response.isSuccessful) throw Exception(response.body?.string() ?: "Request failed")
        JSONObject(response.body?.string() ?: "{}")
    }

    fun captureMetrics(events: List<Any>): Payload {
        // Placeholder: Compute features from input events
        return Payload(mapOf(
            "iki_mean" to 180.0, "iki_std" to 95.0, "typos_per_100" to 9.0, "backspace_rate" to 0.1,
            "avg_word_len" to 3.8, "short_word_ratio" to 0.6, "swipe_speed_mean" to 1200.0,
            "swipe_speed_std" to 550.0, "press_ms_mean" to 140.0, "press_ms_std" to 60.0,
            "path_erraticness" to 0.65, "emoji_ratio" to 0.2, "punct_ratio" to 0.1,
            "vocab_simplicity" to 0.78, "readability_fk" to 2.5, "rtf_ms" to 900.0,
            "dwell_std_ms" to 420.0
        ))
    }
}