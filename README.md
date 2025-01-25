# Cradle - Text Workflow

## Overview
Cradle is a web application that processes text through keyword extraction, summarization, and optional translation.

## Features
- Text keyword extraction
- Text summarization
- Multi-language translation

## Setup
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Download spaCy model: `python -m spacy download en_core_web_sm`
4. Run the backend: `python backend/app.py`
5. Open `frontend/index.html` in a browser

## Tech Stack
- Backend: Python, Flask
- Frontend: HTML, CSS, JavaScript
- Libraries: HuggingFace Transformers, spaCy, RAKE