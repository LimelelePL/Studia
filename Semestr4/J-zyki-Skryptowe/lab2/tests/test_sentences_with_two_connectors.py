import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../app"))

from sentences_with_two_connectors import check_word, count_connectors


# --- check_word ---

def test_check_word_i():
    assert check_word("i") is True

def test_check_word_oraz():
    assert check_word("oraz") is True

def test_check_word_ale():
    assert check_word("ale") is True

def test_check_word_ze():
    assert check_word("że") is True

def test_check_word_lub():
    assert check_word("lub") is True

def test_check_word_not_connector():
    assert check_word("ala") is False

def test_check_word_empty():
    assert check_word("") is False

def test_check_word_partial_match():
    # "lub" to spójnik, ale "luby" już nie
    assert check_word("luby") is False

def test_check_word_iize():
    # "iże" to nie "i" ani "że"
    assert check_word("iże") is False

def test_check_word_albo():
    # "albo" nie jest na liście
    assert check_word("albo") is False

def test_check_word_uppercase_not_handled():
    # check_word oczekuje już lowercase — caller robi .lower()
    assert check_word("I") is False
    assert check_word("Lub") is False


# --- count_connectors ---

def test_count_zero():
    assert count_connectors("ala ma kota") == 0

def test_count_one():
    assert count_connectors("ala i kot") == 1

def test_count_two():
    assert count_connectors("ala i kot lub pies") == 2

def test_count_three():
    assert count_connectors("i oraz ale") == 3

def test_count_all_five():
    assert count_connectors("i oraz ale że lub") == 5

def test_count_empty():
    assert count_connectors("") == 0

def test_count_only_spaces():
    assert count_connectors("   ") == 0

def test_count_case_insensitive():
    # count_connectors robi word.lower() przed check_word
    assert count_connectors("Ala I Lub kot") == 2

def test_count_connector_with_punctuation():
    # "i," — get_next_word zwraca "i" bez przecinka
    assert count_connectors("ala, i kot, lub pies.") == 2

def test_count_connector_not_standalone():
    # "iże" nie powinno być liczone
    assert count_connectors("ala iże kot") == 0

def test_count_connector_at_start():
    assert count_connectors("i ala ma kota") == 1

def test_count_connector_at_end():
    assert count_connectors("ala ma kota i") == 1

def test_count_exactly_two_minimum():
    assert count_connectors("ala i lub") == 2

def test_count_repeated_connector():
    # "i" pojawia się dwukrotnie — liczymy oba
    assert count_connectors("ala i kot i pies") == 2

def test_count_long_sentence_two_connectors():
    sentence = "Szedł przez las " + "bardzo długo " * 20 + "i pola lub góry."
    assert count_connectors(sentence) == 2

def test_count_long_sentence_no_connectors():
    sentence = "Szedł przez las " + "bardzo długo " * 20 + "aż do miasta."
    assert count_connectors(sentence) == 0

def test_count_hyphenated_word_not_connector():
    # "lub-lub" to jeden wyraz z myślnikiem — nie jest spójnikiem "lub"
    assert count_connectors("ala lub-lub pies") == 0

def test_count_connector_after_hyphen():
    # myślnik kończy poprzednie słowo; "lub" po nim jest osobnym wyrazem
    assert count_connectors("coś- lub coś i innego") == 2
