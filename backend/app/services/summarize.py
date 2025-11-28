try:
    from transformers import pipeline
    summarizer = pipeline('summarization', model='facebook/bart-large-cnn')
except Exception:
    summarizer = None

def summarize_text(text: str, max_length: int = 130):
    if summarizer is None:
        return 'Summarizer not available in this environment.'
    out = summarizer(text, max_length=max_length, min_length=30, do_sample=False)
    return out[0]['summary_text']
