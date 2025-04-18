import unittest
from processor import normalize_text, remove_stopwords, count_word_frequency


class TestTextProcessor(unittest.TestCase):

    def test_normalize_text(self):
        self.assertEqual(normalize_text("Hello, World!"), "hello world")

    def test_remove_stopwords(self):
        words = ["this", "is", "a", "test"]
        self.assertEqual(remove_stopwords(words), ["this", "test"])

    def test_count_word_frequency(self):
        text = "The quick brown fox jumps over the lazy dog and the quick blue hare"
        result = count_word_frequency(text)
        expected = {
            "quick": 2,
            "brown": 1,
            "fox": 1,
            "jumps": 1,
            "over": 1,
            "lazy": 1,
            "dog": 1,
            "blue": 1,
            "hare": 1,
        }
        self.assertEqual(result, expected)
