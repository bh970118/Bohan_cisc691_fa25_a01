from authorship_identifier_v01 import clean_word, average_word_length, different_to_total, exactly_once_to_total, split_string

def test_clean_word():
    print(clean_word("Hello!"))         # Expected: 'hello'
    print(clean_word("  Python3.8 "))   # Expected: 'python'
    print(clean_word("123"))            # Expected: ''
    print(clean_word("Test-case."))     # Expected: 'testcase'
    print(clean_word("   "))            # Expected: ''

def test_average_word_length():
    print(average_word_length(["hello", "world"]))          # Expected: 5.0
    print(average_word_length(["a", "ab", "abc"]))          # Expected: 2.0
    print(average_word_length([]))                          # Expected: 0.0
    print(average_word_length([""]))                        # Expected: 0.0
    print(average_word_length(["longword", "s"]))           # Expected: 4.5

def test_different_to_total():
    print(different_to_total(["a", "b", "c", "a"]))         # Expected: 0.75
    print(different_to_total(["x", "x", "x"]))              # Expected: 0.333...
    print(different_to_total([]))                           # Expected: 0.0
    print(different_to_total(["one"]))                      # Expected: 1.0
    print(different_to_total(["a", "b", "b", "c", "c"]))    # Expected: 0.6

def test_exactly_once_to_total():
    print(exactly_once_to_total(["a", "b", "c", "a"]))      # Expected: 0.5
    print(exactly_once_to_total(["x", "x", "x"]))           # Expected: 0.0
    print(exactly_once_to_total([]))                        # Expected: 0.0
    print(exactly_once_to_total(["one"]))                   # Expected: 1.0
    print(exactly_once_to_total(["a", "b", "b", "c", "c"])) # Expected: 0.2

def test_split_string():
    print(split_string("Hello world!"))                     # Expected: ['Hello', 'world!']
    print(split_string("  This is   a test. "))             # Expected: ['This', 'is', 'a', 'test.']
    print(split_string(""))                                 # Expected: []
    print(split_string("singleword"))                       # Expected: ['singleword']
    print(split_string("a b c d e"))                        # Expected: ['a', 'b', 'c', 'd', 'e']

if __name__ == "__main__":
    print("Testing clean_word:")
    test_clean_word()
    print("\nTesting average_word_length:")
    test_average_word_length()
    print("\nTesting different_to_total:")
    test_different_to_total()
    print("\nTesting exactly_once_to_total:")
    test_exactly_once_to_total()
    print("\nTesting split_string:")
    test_split_string()