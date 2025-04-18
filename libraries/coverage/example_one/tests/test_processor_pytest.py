from processor import normalize_text, remove_stopwords, count_word_frequency


def test_normalize_text():
    assert normalize_text("Hello, World!") == "hello world"


def test_remove_stopwords():
    assert remove_stopwords(["a", "quick", "brown", "fox"]) == ["quick", "brown", "fox"]


def test_count_word_frequency():
    text = "Blue sky blue sea and blue dreams"
    result = count_word_frequency(text)
    assert result == {"blue": 3, "sky": 1, "sea": 1, "dreams": 1}
