# Final Project

**Project name:** Final Project  
**Required repository name:** `oaqjp-final-project-emb-ai`  
**Developer:** Thomas Caruso

This repository contains the final project for IBM's **Developing AI Applications with Python and Flask** course. The application sends text to the Watson NLP EmotionPredict endpoint, formats five emotion scores, identifies the dominant emotion, handles invalid input, and exposes the result through a Flask web interface.

## Project structure

```text
.
├── emotion_detection.py
├── EmotionDetection
│   ├── __init__.py
│   └── emotion_detection.py
├── static
│   ├── mywebscript.js
│   └── style.css
├── templates
│   └── index.html
├── screenshots
├── terminal_outputs
├── tools
│   ├── static_analysis.py
│   └── validate_output_format.py
├── .pylintrc
├── README.md
├── requirements.txt
├── server.py
└── test_emotion_detection.py
```

## Install and run

```bash
python3 -m pip install -r requirements.txt
python3 -m unittest test_emotion_detection.py -v
pylint server.py EmotionDetection test_emotion_detection.py
python3 server.py
```

Open `http://localhost:5000` in a browser.

## Watson NLP response format

```python
{
    "anger": 0.05,
    "disgust": 0.05,
    "fear": 0.05,
    "joy": 0.80,
    "sadness": 0.05,
    "dominant_emotion": "joy"
}
```

A Watson HTTP status code of `400` returns the same keys with `None` values.

## Required submission evidence

- `screenshots/6b_deployment_test.png`
- `screenshots/7c_error_handling_interface.png`
- Unit-test, package-validation, output-format, and static-analysis evidence is stored in `terminal_outputs/` and `screenshots/`.
