import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../app"))

from sentences_max_4_words import count_words


def test_empty():
    assert count_words("") == 0

def test_only_spaces():
    assert count_words("   ") == 0

def test_only_punctuation():
    assert count_words("... !!!") == 0

def test_single_word():
    assert count_words("Warszawa") == 1

def test_four_words():
    assert count_words("Ala ma cztery słowa.") == 4

def test_five_words():
    assert count_words("Ala ma pięć różnych słów.") == 5

def test_leading_and_trailing_spaces():
    assert count_words("  ala ma kota  ") == 3

def test_hyphenated_word_counts_as_one():
    # Bielsko-Biała to jeden wyraz
    assert count_words("Mieszkał w Bielsku-Białej.") == 3

def test_apostrophe_word_counts_as_one():
    # O'Brien to jeden wyraz
    assert count_words("Przyszedł O'Brien wczoraj.") == 3

def test_compound_adjective_counts_as_one():
    # biało-czerwony to jeden wyraz złożony
    assert count_words("Miał biało-czerwoną flagę.") == 3

def test_number_not_counted():
    # cyfry nie są literami — nie liczą się jako wyrazy
    assert count_words("Miał 3 koty.") == 2

def test_number_with_hyphen():
    # "19-letni" → "19-" to non-alpha, skip_non_alpha je pomija → "letni" liczy się jako osobny wyraz
    assert count_words("Przyszedł 19-letni chłopiec.") == 3

def test_exactly_four_with_hyphen():
    assert count_words("Mieszkał w Bielsku-Białej dawno.") == 4

def test_five_with_hyphen():
    assert count_words("On mieszkał w Bielsku-Białej dawno.") == 5

def test_multiple_spaces_between_words():
    assert count_words("ala   ma   kota") == 3

def test_comma_does_not_split_word():
    # przecinek nie jest literą, nie tworzy nowego wyrazu
    assert count_words("Ala, kot, pies, mysz.") == 4

def test_long_sentence():
    assert count_words("To jest bardzo długie zdanie z wieloma wyrazami.") == 8
