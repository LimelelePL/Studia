import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../app"))

from percent_senteces_with_proper_name import has_proper_name
from sentence_utils import skip_non_alpha, skip_word


# --- skip_non_alpha ---

def test_skip_non_alpha_leading_spaces():
    assert skip_non_alpha("  hello") == "hello"

def test_skip_non_alpha_leading_punctuation():
    assert skip_non_alpha("...hello") == "hello"

def test_skip_non_alpha_already_alpha():
    assert skip_non_alpha("hello") == "hello"

def test_skip_non_alpha_empty():
    assert skip_non_alpha("") == ""

def test_skip_non_alpha_only_spaces():
    assert skip_non_alpha("   ") == ""

def test_skip_non_alpha_mixed_punctuation():
    assert skip_non_alpha("., !?Słowo") == "Słowo"


# --- skip_word ---

def test_skip_word_basic():
    assert skip_word("hello world") == " world"

def test_skip_word_full_word():
    assert skip_word("hello") == ""

def test_skip_word_starts_with_non_alpha():
    assert skip_word(" hello") == " hello"

def test_skip_word_empty():
    assert skip_word("") == ""

def test_skip_word_polish_chars():
    assert skip_word("Łódź jest") == " jest"

def test_skip_word_hyphen_inside():
    assert skip_word("Bielsko-Biała reszta") == " reszta"

def test_skip_word_hyphen_before_digit():
    # cyfra po myślniku — myślnik kończy słowo
    assert skip_word("Windows-95") == "-95"

def test_skip_word_hyphen_at_end():
    # myślnik na końcu bez kolejnej litery — kończy słowo
    assert skip_word("słowo- reszta") == "- reszta"

def test_skip_word_apostrophe_inside():
    assert skip_word("O'Brien reszta") == " reszta"

def test_skip_word_double_hyphen():
    # podwójny myślnik — pierwszy zatrzymuje (drugi to nie litera)
    assert skip_word("Anna--Maria") == "--Maria"


# --- has_proper_name ---

# Przypadki zwracające False

def test_no_proper_name_all_lowercase():
    assert has_proper_name("ala ma kota.") is False

def test_no_proper_name_only_first_word_uppercase():
    assert has_proper_name("Ala ma kota.") is False

def test_no_proper_name_single_word():
    assert has_proper_name("Warszawa") is False

def test_no_proper_name_empty():
    assert has_proper_name("") is False

def test_no_proper_name_only_spaces():
    assert has_proper_name("   ") is False

def test_no_proper_name_leading_spaces_first_word_uppercase():
    # "Wielka" to pierwsze słowo mimo spacji na początku
    assert has_proper_name("  Wielka vojna między korporacjami") is False

def test_no_proper_name_iphone():
    # iPhone zaczyna się małą literą
    assert has_proper_name("Kupiłem iPhone za dużo.") is False

def test_no_proper_name_after_punctuation_lowercase():
    assert has_proper_name("Wiem, że to prawda.") is False

def test_no_proper_name_two_words_both_lowercase_after_first():
    assert has_proper_name("Szedł przez las i pole.") is False


# Przypadki zwracające True

def test_proper_name_basic():
    assert has_proper_name("Ala ma Kota.") is True

def test_proper_name_leading_spaces():
    # Wielka jest pierwszym słowem, Naka jest nazwą własną
    assert has_proper_name("  Wielka Naka wygrała.") is True

def test_proper_name_after_comma():
    assert has_proper_name("Wiem, Że to działa.") is True

def test_proper_name_polish_uppercase():
    assert has_proper_name("Poszedł do Łodzi na weekend.") is True

def test_proper_name_after_ellipsis():
    assert has_proper_name("I wtedy... Janek przyszedł.") is True

def test_proper_name_after_number():
    # liczba jest nie-alfa, więc "Polska" to początek słowa z wielką literą
    assert has_proper_name("W roku 1918 Polska odzyskała niepodległość.") is True

def test_proper_name_single_char_words():
    # "A" pierwsze słowo, "B" drugie z wielką — nazwa własna
    assert has_proper_name("A i B to litery.") is True

def test_proper_name_all_caps_word():
    assert has_proper_name("Działała firma NATO od lat.") is True

def test_proper_name_after_hyphen():
    # "Anna" po myślniku to nowe słowo z wielką literą
    assert has_proper_name("Mam na myśli Anna-Maria.") is True

def test_proper_name_multiple_proper_names():
    assert has_proper_name("Spotkał Adama i Ewę w Warszawie.") is True

def test_proper_name_only_punctuation_then_uppercase():
    assert has_proper_name("Pierwsza... Druga próba.") is True

def test_proper_name_long_sentence():
    sentence = "Szedł przez " + "bardzo długi las i " * 50 + "Wisłę."
    assert has_proper_name(sentence) is True

def test_no_proper_name_long_sentence():
    sentence = "Szedł przez " + "bardzo długi las i " * 50 + "pole."
    assert has_proper_name(sentence) is False


# --- Myślnik w wyrazach polskich ---

def test_hyphen_compound_adjective_all_lowercase():
    # biało-czerwony to przymiotnik złożony, oba człony małe
    assert has_proper_name("Miała biało-czerwoną flagę.") is False

def test_hyphen_compound_adjective_after_first_word():
    # czarno-biały to nie nazwa własna
    assert has_proper_name("Oglądali czarno-biały film.") is False

def test_hyphen_proper_name_city():
    # Bielsko-Biała — nazwa własna miasta, drugi człon wielką literą
    assert has_proper_name("Mieszkał w Bielsku-Białej przez lata.") is True

def test_hyphen_proper_name_person():
    # Anna-Maria — imię złożone
    assert has_proper_name("Spotkał Annę-Marię na dworcu.") is True

def test_hyphen_compound_uppercase_second_part():
    # Biało-Ruska — przymiotnik od nazwy własnej
    assert has_proper_name("Wyruszyli na Biało-Ruską wyprawę.") is True

def test_hyphen_number_compound_lowercase():
    # 19-letni — cyfra non-alpha, "letni" zaczyna się małą
    assert has_proper_name("Przyszedł 19-letni chłopiec.") is False

def test_hyphen_number_compound_uppercase():
    # 20-Letni — sztucznie, ale sprawdzamy wykrycie
    assert has_proper_name("Przyszedł 20-Letni zawodnik.") is True

def test_hyphen_long_sentence_with_compound_words():
    sentence = "Szedł przez " + "biało-czerwone pola i " * 30 + "Wisłę."
    assert has_proper_name(sentence) is True  # Wisła

def test_hyphen_long_sentence_no_proper_name():
    sentence = "Szedł przez " + "biało-czerwone pola i " * 30 + "rzekę."
    assert has_proper_name(sentence) is False


# --- Apostrof w nazwiskach obcojęzycznych ---

def test_apostrophe_irish_name():
    # O'Brien — apostrof non-alpha, "Brien" zaczyna się wielką
    assert has_proper_name("Przyszedł O'Brien na spotkanie.") is True

def test_apostrophe_lowercase():
    assert has_proper_name("Przyszedł o'clock na spotkanie.") is False


# --- Pauza (—) w dialogach ---

def test_em_dash_uppercase_after():
    # Po pauzie wielka litera — false positive per definicję zadania
    assert has_proper_name("Powiedział — Chodź tu.") is True

def test_em_dash_lowercase_after():
    assert has_proper_name("Powiedział — chodź tu.") is False


# --- Długie zdania z różnymi znakami ---

def test_long_sentence_proper_name_at_end():
    sentence = "Szedł przez " + "bardzo długą drogę do " * 40 + "Warszawy."
    assert has_proper_name(sentence) is True

def test_long_sentence_with_hyphens_proper_name():
    sentence = "Jechał przez " + "biało-czerwone miasto i " * 20 + "Bielsko-Białą."
    assert has_proper_name(sentence) is True

def test_long_sentence_with_hyphens_no_proper_name():
    sentence = "Jechał przez " + "biało-czerwone miasto i " * 20 + "rzekę."
    assert has_proper_name(sentence) is False
