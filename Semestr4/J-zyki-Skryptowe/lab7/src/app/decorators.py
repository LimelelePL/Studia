import inspect
import logging
import time
from collections.abc import Callable
from functools import wraps
from typing import Any


def log(lvl: int = logging.DEBUG):
    def decorator(target: Any):

        @wraps(target)
        def wrapper(*args, **kwargs):
            logging.basicConfig(level=lvl)
            start = time.perf_counter()
            name = target.__name__
            result = target(*args, **kwargs)
            end = time.perf_counter() - start

            if inspect.isclass(target):
                msg = f"UTWORZONO OBIEKT klasy: {name}"
            else:
                msg = f"WYKONANO FUNKCJĘ: {name} | czas startu : {start} | czas trwania: {end:.4f}s"
                f"argumenty: {args} | wynik: {result}"

            logging.log(lvl, msg)
            return result

        return wrapper

    return decorator


def log_test():
    @log(logging.INFO)
    def add(a, b):
        return a + b

    add(1, 2)


def log_test_class():
    @log(logging.INFO)
    class TestClass:
        def __init__(self, field: int):
            self.field = field

    test = TestClass(1)


# napisac dekorator require gdzie dla kazdego argumentu funkcji


def require(target: Callable):
    @wraps(target)
    def wrapper(*args, **kwargs):
        if args:
            for arg in args:
                if arg is None:
                    raise ValueError("argument funkcji jest none")
        if kwargs:
            for kwarg in kwargs.values():
                if kwarg is None:
                    raise ValueError("klucz ma wartość none")
        return target(*args, **kwargs)

    return wrapper

