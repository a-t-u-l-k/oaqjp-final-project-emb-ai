"""Unit tests for the EmotionDetection package."""

from __future__ import annotations

import unittest
from unittest.mock import patch
from urllib import error

from EmotionDetection.emotion_detection import emotion_detector, emotion_predictor


class TestEmotionDetection(unittest.TestCase):
    """Verify the Watson response normalization logic."""

    def test_emotion_predictor_returns_dominant_emotion(self) -> None:
        payload = {
            "emotionPredictions": [
                {
                    "emotion": {
                        "anger": 0.02,
                        "disgust": 0.01,
                        "fear": 0.05,
                        "joy": 0.88,
                        "sadness": 0.04,
                    }
                }
            ]
        }

        result = emotion_predictor(payload)

        self.assertEqual(result["dominant_emotion"], "joy")
        self.assertEqual(result["anger"], 0.02)
        self.assertIsNone(result["error"])

    @patch("EmotionDetection.emotion_detection._request_watson_emotion")
    def test_emotion_detector_handles_valid_text(self, mocked_request) -> None:
        mocked_request.return_value = {
            "emotionPredictions": [
                {
                    "emotion": {
                        "anger": 0.71,
                        "disgust": 0.05,
                        "fear": 0.08,
                        "joy": 0.03,
                        "sadness": 0.13,
                    }
                }
            ]
        }

        result = emotion_detector("I am furious about the delay.")

        self.assertEqual(result["dominant_emotion"], "anger")
        self.assertIsNone(result["error"])

    def test_emotion_detector_rejects_blank_text(self) -> None:
        result = emotion_detector("   ")

        self.assertIsNone(result["dominant_emotion"])
        self.assertEqual(result["error"], "Invalid text! Please try again.")

    @patch("EmotionDetection.emotion_detection._request_watson_emotion")
    def test_emotion_detector_handles_http_400(self, mocked_request) -> None:
        mocked_request.side_effect = error.HTTPError(
            url="https://example.invalid",
            code=400,
            msg="Bad Request",
            hdrs=None,
            fp=None,
        )

        result = emotion_detector("bad input")

        self.assertIsNone(result["dominant_emotion"])
        self.assertEqual(result["error"], "Invalid text! Please try again.")

    @patch("EmotionDetection.emotion_detection._request_watson_emotion")
    def test_emotion_detector_handles_service_unavailable(
        self,
        mocked_request,
    ) -> None:
        mocked_request.side_effect = error.URLError("offline")

        result = emotion_detector("I feel nervous about tomorrow.")

        self.assertIsNone(result["dominant_emotion"])
        self.assertEqual(
            result["error"],
            "Emotion analysis service is unavailable right now.",
        )


if __name__ == "__main__":
    unittest.main()
