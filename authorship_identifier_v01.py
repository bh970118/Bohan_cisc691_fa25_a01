import re
import os
from collections import Counter

def clean_word(word):
    """
    Cleans a word by:
    - Lowercasing
    - Removing punctuation and non-alphabetic characters
    - Stripping leading/trailing whitespace

    Args:
        word (str): The input word.

    Returns:
        str: The cleaned word.
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
    return (
        average_word_length(words),
        different_to_total(words),
        exactly_once_to_total(words)
        )

def get_all_signatures(texts):
    signatures = {}
    for author, text in texts.items():
        words = [clean_word(word) for word in split_string(text) if clean_word(word)]
        signatures[author] = make_signature(words)
    return signatures

def make_guess(unknown_text, signatures):
    words = [clean_word(word) for word in split_string(unknown_text) if clean_word(word)]
    unknown_sig = make_signature(words)
    min_author = None
    min_dist = float('inf')
    for author, sig in signatures.items():
        dist = sum((a - b) ** 2 for a, b in zip(unknown_sig, sig)) ** 0.5
        if dist < min_dist:
            min_dist = dist
            min_author = author
    return min_author

    # --- Inline main logic for testing ---

def read_file(path):
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()

known_files = {
        "Mark Twain": "/Users/bh0118/Desktop/Harrisburg/691/A01/additional_book_files/ch11/known_authors/mark_twain.txt",
        "Jane Austen": "/Users/bh0118/Desktop/Harrisburg/691/A01/additional_book_files/ch11/known_authors/jane_austen.txt",
        "Charles Dickens": "/Users/bh0118/Desktop/Harrisburg/691/A01/additional_book_files/ch11/known_authors/charles_dickens.txt",
        "Arthur Conan Doyle": "/Users/bh0118/Desktop/Harrisburg/691/A01/additional_book_files/ch11/known_authors/Arthur_Conan_Doyle.txt"}

unknown_files = [
        "/Users/bh0118/Desktop/Harrisburg/691/A01/additional_book_files/ch11/unknown1.txt",
        "/Users/bh0118/Desktop/Harrisburg/691/A01/additional_book_files/ch11/unknown2.txt",
        "/Users/bh0118/Desktop/Harrisburg/691/A01/additional_book_files/ch11/unknown3.txt",
        "/Users/bh0118/Desktop/Harrisburg/691/A01/additional_book_files/ch11/unknown4.txt"]

if __name__ == "__main__":
    known_texts = {author: read_file(path) for author, path in known_files.items()}
    signatures = get_all_signatures(known_texts)

    for fname in unknown_files:
        unknown_text = read_file(fname)
        guess = make_guess(unknown_text, signatures)
        print(f"{fname}: {guess}")