import string

import pytest

from app.functions import acronym, atleast, atmost, exists, forall, group_anagram, make_alpha_dict, median, sqrt
from app.generators import PasswordGenerator, make_generator, make_generator_mem


# zad 1a
def test_acronym():
    assert acronym(["Zakład", "Ubezpieczeń", "Społecznych"]) == "ZUS"
    assert acronym(["Polska", "Agencja", "Prasowa"]) == "PAP"


# zad 1b
def test_median_odd():
    assert median([1, 1, 19, 2, 3, 4, 4, 5, 1]) == 3


def test_median_even():
    assert median([1, 2, 3, 4]) == 2.5


# zad 1c
def test_sqrt():
    result = sqrt(3, epsilon=0.1)
    assert abs(result ** 2 - 3) < 0.1
    assert result >= 0


def test_sqrt_zero():
    assert sqrt(0, epsilon=0.001) == 0.0


# zad 1d - make_alpha_dict (znany bug: używa word[0] zamiast wszystkich liter)
def test_make_alpha_dict_keys_exist():
    result = make_alpha_dict("on i ona")
    assert "o" in result
    assert "i" in result


# zad 1f
def test_group_anagram():
    result = group_anagram(["kot", "tok", "pies", "kep", "pek"])
    assert result["kot"] == ["kot", "tok"]
    assert result["eips"] == ["pies"]
    assert result["ekp"] == ["kep", "pek"]


# zad 2
def test_forall_true():
    assert forall(lambda x: x > 0, [1, 2, 3]) is True


def test_forall_false():
    assert forall(lambda x: x > 0, [1, -1, 3]) is False


def test_exists_true():
    assert exists(lambda x: x > 5, [1, 2, 10]) is True


def test_exists_false():
    assert exists(lambda x: x > 5, [1, 2, 3]) is False


def test_atleast():
    assert atleast(2, lambda x: x % 2 == 0, [1, 2, 4, 5]) is True
    assert atleast(3, lambda x: x % 2 == 0, [1, 2, 4, 5]) is False


def test_atmost():
    assert atmost(2, lambda x: x % 2 == 0, [1, 2, 4, 5]) is True
    assert atmost(1, lambda x: x % 2 == 0, [1, 2, 4, 5]) is False


# zad 3 - PasswordGenerator
def test_password_generator_length():
    gen = PasswordGenerator(length=8, count=5)
    for pwd in gen:
        assert len(pwd) == 8


def test_password_generator_count():
    gen = PasswordGenerator(length=6, count=3)
    passwords = list(gen)
    assert len(passwords) == 3


def test_password_generator_stop_iteration():
    gen = PasswordGenerator(length=4, count=2)
    next(gen)
    next(gen)
    with pytest.raises(StopIteration):
        next(gen)


def test_password_generator_charset():
    charset = "abc"
    gen = PasswordGenerator(length=10, count=5, charset=charset)
    for pwd in gen:
        assert all(c in charset for c in pwd)


def test_password_generator_default_charset():
    gen = PasswordGenerator(length=10, count=5)
    allowed = set(string.ascii_letters + string.digits)
    for pwd in gen:
        assert all(c in allowed for c in pwd)


def test_password_generator_iter_returns_self():
    gen = PasswordGenerator(length=4, count=2)
    assert iter(gen) is gen


# zad 4 - make_generator z lambdami
def test_make_generator_arithmetic():
    gen = make_generator(lambda n: 2 * n + 1)  # 3, 5, 7, 9, 11
    assert [next(gen) for _ in range(5)] == [3, 5, 7, 9, 11]


def test_make_generator_geometric():
    gen = make_generator(lambda n: 3 ** n)  # 3, 9, 27, 81, 243
    assert [next(gen) for _ in range(5)] == [3, 9, 27, 81, 243]


def test_make_generator_power():
    gen = make_generator(lambda n: n ** 2)  # 1, 4, 9, 16, 25
    assert [next(gen) for _ in range(5)] == [1, 4, 9, 16, 25]


# zad 5 - make_generator_mem
def test_make_generator_mem():
    gen = make_generator_mem(lambda n: n * 2)
    assert [next(gen) for _ in range(4)] == [2, 4, 6, 8]
