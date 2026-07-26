"""Unit tests for the EmotionDetection package."""

import unittest
from unittest.mock import Mock, patch

from EmotionDetection import emotion_detector


class TestEmotionDetector(unittest.TestCase):
    """Validate dominant-emotion detection and invalid-input handling."""

    @staticmethod
    def _mock_response(dominant_emotion: str) -> Mock:
        """Create a successful mocked Watson response."""
        scores = {
            "anger": 0.05,
            "disgust": 0.05,
            "fear": 0.05,
            "joy": 0.05,
            "sadness": 0.05,
        }
        scores[dominant_emotion] = 0.80

        response = Mock()
        response.status_code = 200
        response.json.return_value = {
            "emotionPredictions": [{"emotion": scores}]
        }
        response.raise_for_status.return_value = None
        return response

    def _assert_dominant(self, text: str, expected: str) -> None:
        """Assert that the specified emotion is returned as dominant."""
        with patch(
            "EmotionDetection.emotion_detection.requests.post",
            return_value=self._mock_response(expected),
        ):
            result = emotion_detector(text)

        self.assertEqual(result["dominant_emotion"], expected)

    def test_joy(self) -> None:
        """Joy should be dominant for a glad statement."""
        self._assert_dominant("I am glad this happened", "joy")

    def test_anger(self) -> None:
        """Anger should be dominant for a mad statement."""
        self._assert_dominant("I am really mad about this", "anger")

    def test_disgust(self) -> None:
        """Disgust should be dominant for a disgusted statement."""
        self._assert_dominant(
            "I feel disgusted just hearing about this",
            "disgust",
        )

    def test_sadness(self) -> None:
        """Sadness should be dominant for a sad statement."""
        self._assert_dominant("I am so sad about this", "sadness")

    def test_fear(self) -> None:
        """Fear should be dominant for an afraid statement."""
        self._assert_dominant(
            "I am really afraid that this will happen",
            "fear",
        )

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_status_code_400(self, mock_post: Mock) -> None:
        """A 400 response should return the required empty result."""
        response = Mock()
        response.status_code = 400
        mock_post.return_value = response

        result = emotion_detector("")

        self.assertEqual(
            result,
            {
                "anger": None,
                "disgust": None,
                "fear": None,
                "joy": None,
                "sadness": None,
                "dominant_emotion": None,
            },
        )


if __name__ == "__main__":
    unittest.main()
