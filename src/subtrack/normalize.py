import re

# Words that appear in bank descriptions but aren't part of the merchant name.
NOISE_WORDS = {"COM", "WWW", "INDIA", "ORDER", "PAY", "PAYMENT"}


def normalize_merchant(description: str) -> str:
    """Turn 'NETFLIX.COM 8007' into 'Netflix'."""
    letters_only = re.sub(r"[^A-Za-z]+", " ", description).upper()
    words = [w for w in letters_only.split() if w not in NOISE_WORDS]
    return " ".join(words).title() or description.strip().title()