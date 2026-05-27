import random
import string
from collections.abc import Callable, Generator
from functools import cache


# zad 4
def make_generator(f: Callable) -> Generator:
    n = 1
    while True:
        yield f(n)
        n += 1


# nalezy uzyc dekoratora cache zeby wywolania rekurencyjne szly do cache a nie na stos
@cache
def fib(n: int) -> int:
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)


def test_gen():
    gen = make_generator(fib)
    print(next(gen))
    print(next(gen))
    print(next(gen))
    print(next(gen))


# zad 5
def make_generator_mem(f: Callable):
    return make_generator(cache(f))


def test_mem_gen():
    gen = make_generator_mem(fib)
    print(next(gen))
    print(next(gen))
    print(next(gen))
    print(next(gen))


# zad 3
class PasswordGenerator:
    def __init__(
        self,
        length: int,
        charset: str = string.ascii_letters + string.digits,
        count: int = 10,
    ):
        self.length = length
        self.charset = charset
        self.count = count
        self._generated = 0

    def __iter__(self):
        return self

    def __next__(self) -> str:
        if self._generated >= self.count:
            raise StopIteration
        self._generated += 1
        return "".join(random.choices(self.charset, k=self.length))


def demo_password_generator() -> None:
    # a) jawne wywołanie next()
    gen = PasswordGenerator(length=8, count=3)
    print(next(gen))
    print(next(gen))
    print(next(gen))

    # b) pętla for
    for password in PasswordGenerator(length=12, count=4):
        print(password)
