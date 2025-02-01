from transformers import pipeline

summarizer = pipeline("summarization")

def simple_summarize(text):
    return summarizer(text, max_length=50, min_length=25, do_sample=False)[0]['summary_text']
