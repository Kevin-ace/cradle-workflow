import spacy

def extract_keywords(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    keywords = [chunk.text for chunk in doc.noun_chunks]
    return list(set(keywords))
