# Final Project - Emotion Detector

This Final Project is an Emotion Detector web application that submits user
text to the Watson NLP emotion classification service, formats the emotion
scores, and returns the dominant emotion. If the optional `watson_nlp` runtime
and model are installed locally, the package will try the native library first
and fall back to the hosted endpoint otherwise.


## Project structure

```text
EmotionDetection/
  __init__.py
  emotion_detection.py
static/
  script.js
  style.css
templates/
  index.html
tests/
  test_emotion_detection.py
server.py
pyproject.toml
```

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Run the web application

```bash
source .venv/bin/activate
python server.py
```

Then open `http://127.0.0.1:5000`.

## Run unit tests

```bash
source .venv/bin/activate
python -m unittest discover -s tests
```

## Run static code analysis

```bash
source .venv/bin/activate
pylint EmotionDetection server.py tests
```
