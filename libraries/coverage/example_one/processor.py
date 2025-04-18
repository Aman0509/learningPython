import string

STOPWORDS = {"the", "is", "and", "to", "in", "of", "a"}


def normalize_text(text: str) -> str:
    """Lowercase and remove punctuation from text."""
    return text.lower().translate(str.maketrans("", "", string.punctuation))


def remove_stopwords(words: list[str]) -> list[str]:
    """Remove common stopwords from a list of words."""
    return [word for word in words if word not in STOPWORDS]


def count_word_frequency(text: str) -> dict[str, int]:
    """Return a word frequency dictionary from text."""
    normalized = normalize_text(text)
    words = normalized.split()
    cleaned_words = remove_stopwords(words)
    freq = {}
    for word in cleaned_words:
        freq[word] = freq.get(word, 0) + 1
    return freq
