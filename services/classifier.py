import re

def classify_ticket(text: str) -> str:
    """Baseline classifier to categorize tickets."""
    text_lower = text.lower()
    
    # Simple keyword-based classification
    if any(word in text_lower for word in ["invoice", "pay", "credit card", "billing", "charge"]):
        return "Billing"
    elif any(word in text_lower for word in ["lawsuit", "sue", "legal", "compliance", "gdpr", "nda"]):
        return "Legal"
    else:
        # Defaulting to Technical if other keywords aren't found
        return "Technical"

def check_urgency(text: str) -> float:
    """Regex-based heuristic for urgency."""
    # Searching for flags like "broken" or "ASAP"
    pattern = re.compile(r'\b(broken|asap|urgent|down|crash)\b', re.IGNORECASE)
    if pattern.search(text):
        return 1.0
    else:
        return 0.0