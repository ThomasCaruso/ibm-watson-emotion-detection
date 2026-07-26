"""Demonstrate the required response format without making a network call."""

from unittest.mock import Mock, patch

from EmotionDetection import emotion_detector


response = Mock()
response.status_code = 200
response.json.return_value = {
    "emotionPredictions": [
        {
            "emotion": {
                "anger": 0.04,
                "disgust": 0.01,
                "fear": 0.03,
                "joy": 0.89,
                "sadness": 0.03,
            }
        }
    ]
}
response.raise_for_status.return_value = None

with patch(
    "EmotionDetection.emotion_detection.requests.post",
    return_value=response,
):
    print(emotion_detector("I am glad this happened"))
