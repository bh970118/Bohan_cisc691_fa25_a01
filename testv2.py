import pytest
from authorship_identifier_v01 import get_all_signatures, make_signature, make_guess
import sys
from io import StringIO

def test_make_signature_basic():
    words = ["hello", "world", "hello", "python"]
    sig = make_signature(words)
    # average_word_length: (5+5+5+6)/4 = 5.25
    # different_to_total: 3/4 = 0.75
    # exactly_once_to_total: 2/4 = 0.5 ("world", "python" appear once)
    assert pytest.approx(sig[0], 0.01) == 5.25
    assert pytest.approx(sig[1], 0.01) == 0.75
    assert pytest.approx(sig[2], 0.01) == 0.5

def test_make_signature_empty():
    words = []
    sig = make_signature(words)
    assert sig == (0.0, 0.0, 0.0)

def test_get_all_signatures_basic():
    texts = {
        "Alice": "Hello world hello python",
        "Bob": "Python is great and python is fun"
    }
    sigs = get_all_signatures(texts)
    assert "Alice" in sigs and "Bob" in sigs
    # Alice: ["hello", "world", "hello", "python"]
    assert pytest.approx(sigs["Alice"][0], 0.01) == 5.25
    # Bob: ["python", "is", "great", "and", "python", "is", "fun"]
    # avg len: (6+2+5+3+6+2+3)/7 = 3.857
    assert pytest.approx(sigs["Bob"][0], 0.01) == 3.857

def test_get_all_signatures_empty_text():
    texts = {"Author": ""}
    sigs = get_all_signatures(texts)
    assert sigs["Author"] == (0.0, 0.0, 0.0)

def test_make_guess_correct_author():
    texts = {
        "Alice": "Hello world hello python",
        "Bob": "Python is great and python is fun"
    }
    sigs = get_all_signatures(texts)
    unknown = "Hello python"
    guess = make_guess(unknown, sigs)
    assert guess == "Alice"

def test_make_guess_tie_breaker():
    texts = {
        "A": "a a a a",
        "B": "b b b b"
    }
    sigs = get_all_signatures(texts)
    unknown = "a a a a"
    guess = make_guess(unknown, sigs)
    assert guess == "A"

def test_make_guess_empty_unknown():
    texts = {
        "A": "a a a a",
        "B": "b b b b"
    }
    sigs = get_all_signatures(texts)
    unknown = ""
    guess = make_guess(unknown, sigs)
    assert guess in sigs  # Should return one of the authors

def test_make_guess_no_signatures():
    sigs = {}
    unknown = "test text"
    guess = make_guess(unknown, sigs)
    assert guess is None

if __name__ == "__main__":
        # Run pytest and print output to console
    sys.exit(pytest.main([__file__]))