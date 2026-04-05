"""Helpers for calling the Watson NLP emotion classification endpoint."""

from __future__ import annotations

import json
import os
from typing import Any
from urllib import error, request

try:
    import watson_nlp
except ImportError:  # pragma: no cover - optional dependency
    watson_nlp = None

WATSON_EMOTION_URL = (
    "https://sn-watson-emotion.labs.skills.network/"
    "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
)
WATSON_HTTP_MODEL_ID = "emotion_aggregated-workflow_lang_en_stock"
WATSON_LIBRARY_MODEL_ID = os.getenv(
    "WATSON_NLP_MODEL_ID",
    "emotion_aggregated-workflow_en_stock",
)
EMOTION_KEYS = ("anger", "disgust", "fear", "joy", "sadness")


def _empty_result(error_message: str | None = None) -> dict[str, Any]:
    """Return a normalized empty result."""

    result = {emotion: None for emotion in EMOTION_KEYS}
    result["dominant_emotion"] = None
    result["error"] = error_message
    return result


def _request_watson_http(text_to_analyze: str) -> dict[str, Any]:
    """Submit text to the hosted Watson endpoint and return the raw payload."""

    payload = json.dumps(
        {"raw_document": {"text": text_to_analyze}},
    ).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
        "grpc-metadata-mm-model-id": WATSON_HTTP_MODEL_ID,
    }
    http_request = request.Request(
        WATSON_EMOTION_URL,
        data=payload,
        headers=headers,
        method="POST",
    )
    with request.urlopen(http_request, timeout=15) as response:
        return json.loads(response.read().decode("utf-8"))


def _request_watson_library(text_to_analyze: str) -> dict[str, Any]:
    """Run the optional local Watson NLP model when it is installed."""

    if watson_nlp is None:  # pragma: no cover - depends on optional dependency
        raise ModuleNotFoundError("watson_nlp is not installed.")

    emotion_model = watson_nlp.load(WATSON_LIBRARY_MODEL_ID)
    result = emotion_model.run(text_to_analyze)
    if isinstance(result, dict):
        return result
    if hasattr(result, "to_dict"):
        return result.to_dict()
    return json.loads(json.dumps(result, default=lambda value: value.__dict__))


def _request_watson_emotion(text_to_analyze: str) -> dict[str, Any]:
    """Run Watson emotion detection with local-library fallback support."""

    if watson_nlp is not None:  # pragma: no branch - fallback is intentional
        try:
            return _request_watson_library(text_to_analyze)
        except (AttributeError, OSError, RuntimeError, TypeError, ValueError):
            pass
    return _request_watson_http(text_to_analyze)


def emotion_predictor(payload: dict[str, Any]) -> dict[str, Any]:
    """Convert the Watson payload into a flat emotion summary."""

    predictions = payload.get("emotionPredictions") or payload.get(
        "emotion_predictions",
    ) or []
    if not predictions:
        return _empty_result("Emotion service returned no predictions.")

    emotions = predictions[0].get("emotion") or {}
    if not all(emotion in emotions for emotion in EMOTION_KEYS):
        return _empty_result("Emotion service returned an unexpected payload.")

    dominant_emotion = max(EMOTION_KEYS, key=lambda key: emotions[key])
    result = {emotion: emotions[emotion] for emotion in EMOTION_KEYS}
    result["dominant_emotion"] = dominant_emotion
    result["error"] = None
    return result


def emotion_detector(text_to_analyze: str) -> dict[str, Any]:
    """Run emotion detection and return a normalized result dictionary."""

    if not text_to_analyze or not text_to_analyze.strip():
        return _empty_result("Invalid text! Please try again.")

    error_message = None
    try:
        raw_response = _request_watson_emotion(text_to_analyze.strip())
    except error.HTTPError as exc:
        if exc.code == 400:
            error_message = "Invalid text! Please try again."
        else:
            error_message = "Emotion analysis service returned an HTTP error."
    except error.URLError:
        error_message = "Emotion analysis service is unavailable right now."
    except TimeoutError:
        error_message = "Emotion analysis service timed out."
    except json.JSONDecodeError:
        error_message = "Emotion analysis service returned invalid JSON."

    if error_message is not None:
        return _empty_result(error_message)
    return emotion_predictor(raw_response)
