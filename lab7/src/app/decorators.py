import inspect
import logging
import time
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
