"""Flask application for the Emotion Detector project."""

from __future__ import annotations

from flask import Flask, jsonify, render_template, request

from EmotionDetection import emotion_detector

app = Flask(__name__)


def _format_response(result: dict[str, object]) -> str:
    """Render a normalized emotion response into user-facing text."""

    return (
        "For the given statement, the system response is "
        f"'anger': {result['anger']}, "
        f"'disgust': {result['disgust']}, "
        f"'fear': {result['fear']}, "
        f"'joy': {result['joy']} and "
        f"'sadness': {result['sadness']}. "
        f"The dominant emotion is {result['dominant_emotion']}."
    )


@app.get("/")
def render_index_page() -> str:
    """Render the single-page web client."""

    return render_template("index.html")


@app.get("/emotionDetector")
def run_emotion_detection() -> tuple[str, int] | str:
    """Analyze the supplied text and return a plain-text summary."""

    text_to_analyze = request.args.get("textToAnalyze", default="", type=str)
    result = emotion_detector(text_to_analyze)
    if result["dominant_emotion"] is None:
        return str(result["error"]), 400
    return _format_response(result)


@app.get("/api/emotionDetector")
def run_emotion_detection_api():
    """Expose the normalized result as JSON for programmatic callers."""

    text_to_analyze = request.args.get("textToAnalyze", default="", type=str)
    result = emotion_detector(text_to_analyze)
    status_code = 200 if result["dominant_emotion"] is not None else 400
    return jsonify(result), status_code


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
