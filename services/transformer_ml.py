from transformers import pipeline

# Load lightweight models to save RAM/Time during the hackathon
print("Loading Transformer models... this might take a minute.")
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

def predict_category(text: str) -> str:
    """Transformer-based routing."""
    candidate_labels = ["Billing", "Technical", "Legal"]
    result = classifier(text, candidate_labels)
    # Returns the highest scoring category
    return result["labels"][0]

def calculate_urgency_score(text: str) -> float:
    """Generates a continuous urgency score S in [0, 1]."""
    result = sentiment_analyzer(text)[0]
    # If sentiment is NEGATIVE, we treat it as higher urgency.
    # This is a hackathon shortcut for regression-based urgency.
    score = result["score"]
    if result["label"] == "NEGATIVE":
        # Map high negative confidence to high urgency (close to 1)
        return round(score, 3) 
    else:
        # Map positive confidence to low urgency (close to 0)
        return round(1.0 - score, 3)