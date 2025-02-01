import nltk
import os
import sys

# Ensure NLTK data is downloaded comprehensively
def download_nltk_resources():
    try:
        # Set a custom download directory in the project
        nltk_data_dir = os.path.join(os.path.dirname(__file__), '..', 'nltk_data')
        os.makedirs(nltk_data_dir, exist_ok=True)
        
        # Add the custom directory to NLTK data path
        nltk.data.path.append(nltk_data_dir)
        
        # Download comprehensive NLTK resources
        nltk_resources = [
            'punkt',      # Tokenization
            'stopwords',  # Stop words
            'averaged_perceptron_tagger',  # Part-of-speech tagging
        ]
        
        for resource in nltk_resources:
            try:
                nltk.download(resource, download_dir=nltk_data_dir)
                print(f"Successfully downloaded {resource}")
            except Exception as e:
                print(f"Error downloading {resource}: {e}")
        
        return True
    except Exception as e:
        print(f"Critical error in NLTK resource download: {e}")
        return False

# Attempt to download resources immediately
download_nltk_resources()

from flask import Flask, request, jsonify
from flask_cors import CORS
from rake_nltk import Rake
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
from langdetect import detect

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize RAKE for keyword extraction
try:
    rake = Rake()
except Exception as e:
    print(f"Error initializing RAKE: {e}")
    rake = None

# Supported languages
SUPPORTED_LANGUAGES = {
    'en': 'English',
    'es': 'Spanish', 
    'fr': 'French',
    'de': 'German'
}

def extract_keywords(text, num_keywords=5):
    """Extract top keywords from text using multiple methods"""
    keywords = []
    
    # Method 1: RAKE
    try:
        if rake:
            rake.extract_keywords_from_text(text)
            rake_keywords = rake.get_ranked_phrases()[:num_keywords]
            keywords.extend(rake_keywords)
    except Exception as e:
        print(f"RAKE keyword extraction error: {e}")
    
    # Method 2: Frequency-based keyword extraction
    try:
        # Tokenize and remove stopwords
        stop_words = set(stopwords.words('english'))
        words = word_tokenize(text.lower())
        filtered_words = [word for word in words if word.isalnum() and word not in stop_words]
        
        # Get word frequencies
        freq_dist = FreqDist(filtered_words)
        freq_keywords = [word for word, _ in freq_dist.most_common(num_keywords)]
        keywords.extend(freq_keywords)
    except Exception as e:
        print(f"Frequency-based keyword extraction error: {e}")
    
    # Remove duplicates and limit to num_keywords
    keywords = list(dict.fromkeys(keywords))[:num_keywords]
    
    return keywords

def simple_summarize(text, num_sentences=2):
    """Create a simple extractive summary"""
    try:
        sentences = sent_tokenize(text)
        return ' '.join(sentences[:num_sentences])
    except Exception as e:
        print(f"Summarization error: {e}")
        return text  # Fallback to original text if tokenization fails

def translate_text(text, target_lang='en'):
    """Placeholder for translation (you can replace with a real translation service)"""
    # For now, just return the original text
    return text

@app.route('/process', methods=['POST', 'OPTIONS'])
def process_text():
    # Handle OPTIONS request for CORS preflight
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    try:
        data = request.json
        text = data.get('text', '').strip()
        
        # Add detailed logging
        print(f"Received text for processing: {text}")
        print(f"Received language: {data.get('language', 'en')}")
        
        if not text:
            print("Error: Empty text received")
            return jsonify({'error': 'Text is required'}), 400
        
        # Detect source language
        try:
            src_lang = detect(text)
            print(f"Detected source language: {src_lang}")
        except Exception as lang_detect_error:
            print(f"Language detection error: {lang_detect_error}")
            src_lang = 'en'
        
        # Get target language (default to English)
        tgt_lang = data.get('language', 'en').lower()
        print(f"Target language: {tgt_lang}")
        
        if tgt_lang not in SUPPORTED_LANGUAGES:
            print(f"Unsupported language: {tgt_lang}")
            return jsonify({
                'error': f"Unsupported language. Supported languages are: {', '.join(SUPPORTED_LANGUAGES.keys())}"
            }), 400
        
        # Process text
        try:
            keywords = extract_keywords(text)
            print(f"Extracted keywords: {keywords}")
        except Exception as keyword_error:
            print(f"Keyword extraction error: {keyword_error}")
            keywords = []
        
        try:
            summary = simple_summarize(text)
            print(f"Generated summary: {summary}")
        except Exception as summary_error:
            print(f"Summarization error: {summary_error}")
            summary = ''
        
        try:
            translation = translate_text(summary, tgt_lang)
            print(f"Generated translation: {translation}")
        except Exception as translation_error:
            print(f"Translation error: {translation_error}")
            translation = ''
        
        return jsonify({
            'keywords': keywords,
            'summary': summary,
            'translation': translation,
            'source_language': src_lang,
            'target_language': SUPPORTED_LANGUAGES[tgt_lang]
        })
    
    except Exception as e:
        print(f"Unexpected processing error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)