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

## MODYFIKACJA BOGOACZ - napisać dekroator który zwraca ilość wywołań funkcji

def call_count(func: Any):
    def 