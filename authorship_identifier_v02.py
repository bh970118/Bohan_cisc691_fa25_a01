import re
import os
from collections import Counter
import numpy as np


def clean_word(word):
    """
    Cleans a word by:
    - Lowercasing
    - Removing punctuation and non-alphabetic characters
    - Stripping leading/trailing whitespace
    """
    word = word.lower()
    word = re.sub(r'[^a-z]', '', word)
    return word.strip()

def average_word_length(words):
    if not words:
        return 0.0
    total_length = sum(len(word) for word in words)
    return total_length / len(words)

def different_to_total(words):
    if not words:
        return 0.0
    unique_words = set(words)
    return len(unique_words) / len(words)

def exactly_once_to_total(words):
    if not words:
        return 0.0
    word_counts = Counter(words)
    once_count = sum(1 for count in word_counts.values() if count == 1)
    return once_count / len(words)

def split_string(text):
    return text.split()

def make_signature(words):
    """
    IMPROVEMENT: Adds more stylometric features for better author discrimination.
    """
    total_words = len(words)
    unique_words = len(set(words))
    avg_word_len = average_word_length(words)
    diff_to_total = different_to_total(words)
    once_to_total = exactly_once_to_total(words)
    # Additional metrics:
    # 1. Proportion of words longer than 7 letters
    long_words = sum(1 for w in words if len(w) > 7)
    prop_long_words = long_words / total_words if total_words else 0.0
    
     # 2. Proportion of short words (<=3 letters)
    short_words = sum(1 for w in words if len(w) <= 3)
    prop_short_words = short_words / total_words if total_words else 0.0
   
    # 3. Ratio of unique long words to unique words
    unique_long_words = len(set(w for w in words if len(w) > 7))
    unique_long_ratio = unique_long_words / unique_words if unique_words else 0.0
    
    '''
    # 4. Hapax Legomena Ratio (words that occur once / unique words)
    hapax_legomena = sum(1 for count in Counter(words).values() if count == 1)
    hapax_legomena_ratio = hapax_legomena / unique_words if unique_words else 0.0
    
    # 5. Type-Token Ratio (unique words / total words)
    type_token_ratio = unique_words / total_words if total_words else 0.0
    '''
    return (
        avg_word_len,
        diff_to_total,
        once_to_total,
        prop_long_words,
        prop_short_words,
        unique_long_ratio
    )

def get_all_signatures(texts):
    """
    Returns a dictionary of author:signature tuples.
    """
    signatures = {}
    for author, text in texts.items():
        words = [clean_word(word) for word in split_string(text) if clean_word(word)]
        signatures[author] = make_signature(words)
    return signatures

def normalize_signatures(signatures):
    """
    IMPROVEMENT: Normalizes each feature in the signature to [0, 1] range across all authors.
    Returns a new dictionary of normalized signatures.
    """
    sig_matrix = np.array(list(signatures.values()))
    mins = sig_matrix.min(axis=0)
    maxs = sig_matrix.max(axis=0)
    norm_sigs = {}
    for author, sig in signatures.items():
        norm = [(s - mn) / (mx - mn) if mx > mn else 0.0 for s, mn, mx in zip(sig, mins, maxs)]
        norm_sigs[author] = tuple(norm)
    return norm_sigs, mins, maxs

def normalize_signature(sig, mins, maxs):
    """
    Normalizes a single signature using mins and maxs from known signatures.
    """
    return tuple((s - mn) / (mx - mn) if mx > mn else 0.0 for s, mn, mx in zip(sig, mins, maxs))
# IMPROVEMENT: Use weighted Euclidean distance for better feature importance handling
# Weights can be tuned based on feature importance
FEATURE_WEIGHTS = [8, 18,8, 1, 1, 15]

def make_guess(unknown_text, norm_signatures, mins, maxs, weights=None):
    words = [clean_word(word) for word in split_string(unknown_text) if clean_word(word)]
    unknown_sig = make_signature(words)
    unknown_sig_norm = normalize_signature(unknown_sig, mins, maxs)
    min_author = None
    min_dist = float('inf')
    for author, sig in norm_signatures.items():
        # Apply weights to each feature difference
        dist = sum(weights[i] * (a - b) ** 2 for i, (a, b) in enumerate(zip(unknown_sig_norm, sig))) ** 0.5
        if dist < min_dist:
            min_dist = dist
            min_author = author
    return min_author



def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

known_files = {
    "Mark Twain": "/Users/bh0118/Desktop/Harrisburg/691/A01/additional_book_files/ch11/known_authors/mark_twain.txt",
    "Jane Austen": "/Users/bh0118/Desktop/Harrisburg/691/A01/additional_book_files/ch11/known_authors/jane_austen.txt",
    "Charles Dickens": "/Users/bh0118/Desktop/Harrisburg/691/A01/additional_book_files/ch11/known_authors/charles_dickens.txt",
    "Arthur Conan Doyle": "/Users/bh0118/Desktop/Harrisburg/691/A01/additional_book_files/ch11/known_authors/Arthur_Conan_Doyle.txt"
}

unknown_files = [
    "/Users/bh0118/Desktop/Harrisburg/691/A01/additional_book_files/ch11/unknown1.txt",
    "/Users/bh0118/Desktop/Harrisburg/691/A01/additional_book_files/ch11/unknown2.txt",
    "/Users/bh0118/Desktop/Harrisburg/691/A01/additional_book_files/ch11/unknown3.txt",
    "/Users/bh0118/Desktop/Harrisburg/691/A01/additional_book_files/ch11/unknown4.txt"
]

if __name__ == "__main__":
    # Read known texts and compute signatures
    known_texts = {author: read_file(path) for author, path in known_files.items()}
    signatures = get_all_signatures(known_texts)
    # IMPROVEMENT: Normalize signatures for fair feature comparison
    norm_signatures, mins, maxs = normalize_signatures(signatures)

    for fname in unknown_files:
        unknown_text = read_file(fname)
        guess = make_guess(unknown_text, norm_signatures, mins, maxs, weights=FEATURE_WEIGHTS)
        print(f"{fname}: {guess}")

'''
# Debug module to print intermediate values
if __name__ == "__main__":

    # Read known texts and compute signatures
    known_texts = {author: read_file(path) for author, path in known_files.items()}
    signatures = get_all_signatures(known_texts)
    # Normalize signatures for fair feature comparison
    norm_signatures, mins, maxs = normalize_signatures(signatures)

    # Print normalized signatures for known authors
    print("Normalized signatures for known authors:")
    for author, sig in norm_signatures.items():
        print(f"{author}: {sig}")

    for fname in unknown_files:
        unknown_text = read_file(fname)
        words = [clean_word(word) for word in split_string(unknown_text) if clean_word(word)]
        unknown_sig = make_signature(words)
        unknown_sig_norm = normalize_signature(unknown_sig, mins, maxs)
        print(f"\n{fname} normalized signature: {unknown_sig_norm}")
        guess = make_guess(unknown_text, norm_signatures, mins, maxs)
        print(f"{fname}: {guess}")
'''
