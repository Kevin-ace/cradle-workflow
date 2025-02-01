# Cradle - Intelligent Text Processing Workflow

## Overview
Cradle is an advanced web application designed to provide intelligent text processing capabilities, including keyword extraction, text summarization, and multi-language translation. Leveraging state-of-the-art natural language processing techniques, Cradle helps users derive insights and understand text more effectively.

## Features
- Keyword Extraction: Identify the most important keywords in a given text
- Text Summarization: Generate concise summaries of long-form content
- Multi-language Translation: Translate text between various languages

## Prerequisites
- Python 3.8+
- pip
- Git


## Project Structure
```
Cradle/
│
├── Backend/                # Python Flask backend
│   ├── app.py              # Main application file
│   └── services/           # NLP service modules
│       ├── keyword_extraction.py
│       ├── summarization.py
│       └── translation.py
│
├── Frontend/               # Web interface
│   ├── index.html
│   ├── script.js
│   └── styles.css
│
├── nltk_data/              # NLTK downloaded resources
├── requirements.txt        # Python dependencies
└── README.md
```

## Tech Stack
- Backend: 
  - Python
  - Flask
  - spaCy
  - NLTK
  - HuggingFace Transformers
- Frontend: 
  - HTML5
  - CSS3
  - Vanilla JavaScript
