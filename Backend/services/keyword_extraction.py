import re
from typing import List
from collections import Counter

def extract_keywords(text: str) -> List[str]:
    """
    Extract keywords from the given text using a simple extraction method.
    
    Args:
        text (str): Input text to extract keywords from.
    
    Returns:
        List[str]: Unique keywords extracted from the text.
    
    Raises:
        ValueError: If input is not a string or is empty.
    """
    # Validate input
    if not isinstance(text, str):
        raise ValueError("Input must be a string")
    
    if not text.strip():
        return []
    
    # Convert to lowercase and remove punctuation
    text = re.sub(r'[^\w\s]', '', text.lower())
    
    # Split into words
    words = text.split()
    
    # Remove common stop words
    stop_words = set(['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'])
    words = [word for word in words if word not in stop_words]
    
    # Count word frequencies
    word_freq = Counter(words)
    
    # Select top keywords (words that appear more than once)
    keywords = [word for word, count in word_freq.items() if count > 1]
    
    # If no keywords found, return top 3 most frequent words
    if not keywords:
        keywords = [word for word, _ in word_freq.most_common(3)]
    
    return list(set(keywords))
