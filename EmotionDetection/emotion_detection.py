"""Watson NLP emotion detection client."""

from typing import Any

import requests

EMOTION_URL = (
    "https://sn-watson-emotion.labs.skills.network/"
    "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
)
EMOTION_HEADERS = {
    "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
}


def _empty_emotion_result() -> dict[str, float | str | None]:
    """Return the required response structure for invalid input."""
    return {
        "anger": None,
        "disgust": None,
        "fear": None,
        "joy": None,
        "sadness": None,
        "dominant_emotion": None,
    }


def emotion_detector(text_to_analyze: str) -> dict[str, Any]:
    """Analyze text and return five emotion scores and the dominant emotion."""
    input_json = {"raw_document": {"text": text_to_analyze}}

    response = requests.post(
        EMOTION_URL,
        json=input_json,
        headers=EMOTION_HEADERS,
        timeout=30,
    )

    if response.status_code == 400:
        return _empty_emotion_result()

    response.raise_for_status()
    formatted_response = response.json()
    emotions = formatted_response["emotionPredictions"][0]["emotion"]

    result = {
        "anger": emotions["anger"],
        "disgust": emotions["disgust"],
        "fear": emotions["fear"],
        "joy": emotions["joy"],
        "sadness": emotions["sadness"],
    }
    result["dominant_emotion"] = max(result, key=result.get)
    return result
