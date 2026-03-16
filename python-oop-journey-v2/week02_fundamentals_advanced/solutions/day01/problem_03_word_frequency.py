"""Reference solution for Problem 03: Word Frequency."""

from __future__ import annotations

import string
from pathlib import Path


def word_frequency(filepath: str | Path) -> dict[str, int]:
    """Count word frequencies in a text file.

    Args:
        filepath: Path to the text file.

    Returns:
        Dictionary mapping lowercase words to their frequency count.
        Returns empty dict for empty or non-existent files.
    """
    path = Path(filepath)
    
    if not path.exists():
        return {}
    
    frequencies: dict[str, int] = {}
    
    with open(path, 'r') as f:
        for line in f:
            # Remove punctuation and convert to lowercase
            cleaned = line.lower()
            for punct in string.punctuation:
                cleaned = cleaned.replace(punct, ' ')
            
            # Split into words and count
            for word in cleaned.split():
                if word:  # Skip empty strings
                    frequencies[word] = frequencies.get(word, 0) + 1
    
    return dict(sorted(frequencies.items()))
