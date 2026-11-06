# Cheatsheet - Lista 7

## Temat

Elementy programowania funkcyjnego w Pythonie:

- funkcje jako argumenty
- `lambda`
- `map`, `filter`, `reduce`
- iteratory i generatory
- domknięcia
- memoizacja
- dekoratory
- `logging`

---

## Szybkie zasady

```python
# funkcja jest "normalną" wartością
def square(x: int) -> int:
    return x * x

f = square
print(f(4))  # 16

# lambda - dobra do krótkich funkcji
triple = lambda x: x * 3

# często w liście 7 lepiej używać:
# - generator expressions
# - comprehensions
# - any/all/sum/min/max
# zamiast ręcznych for/while
```

---

## `lambda`

```python
is_even = lambda x: x % 2 == 0
add = lambda a, b: a + b
first_char = lambda s: s[0]

print(is_even(4))      # True
print(add(2, 3))       # 5
print(first_char("kot"))  # "k"
```

Używaj `lambda`, gdy funkcja jest krótka i jednorazowa.

---

## `map`, `filter`, `reduce`

```python
from functools import reduce

numbers = [1, 2, 3, 4, 5]

squares = list(map(lambda x: x * x, numbers))
evens = list(filter(lambda x: x % 2 == 0, numbers))
total = reduce(lambda acc, x: acc + x, numbers, 0)

print(squares)  # [1, 4, 9, 16, 25]
print(evens)    # [2, 4]
print(total)    # 15
```

W praktyce często czytelniejsze są comprehensions:

```python
squares = [x * x for x in numbers]
evens = [x for x in numbers if x % 2 == 0]
```

---

## Przydatne funkcje w stylu funkcyjnym

```python
numbers = [1, 2, 3, 4, 5]

sum(numbers)                     # 15
min(numbers)                     # 1
max(numbers)                     # 5
all(x > 0 for x in numbers)      # True
any(x % 2 == 0 for x in numbers) # True

words = ["ala", "ma", "kota"]
max(words, key=len)              # "kota"
sorted(words, key=len)           # ["ma", "ala", "kota"]
```

---

## Wzorce pod zadania

### Akronim z listy słów

```python
def acronym(words: list[str]) -> str:
    return "".join(word[0] for word in words if word)


print(acronym(["Zaklad", "Ubezpieczen", "Spolecznych"]))  # ZUS
```

### Mediana bez `statistics`

```python
def median(values: list[float]) -> float:
    ordered = sorted(values)
    n = len(ordered)
    mid = n // 2

    if n % 2 == 1:
        return ordered[mid]
    return (ordered[mid - 1] + ordered[mid]) / 2
```

### Pierwiastek metodą Newtona

```python
def sqrt_newton(x: float, epsilon: float = 1e-10) -> float:
    if x < 0:
        raise ValueError("x musi byc >= 0")
    if x == 0:
        return 0.0

    guess = x
    while abs(guess * guess - x) > epsilon:
        guess = (guess + x / guess) / 2
    return guess
```

### `atleast` / `atmost`

```python
from collections.abc import Callable, Iterable


def atleast[T](n: int, pred: Callable[[T], bool], iterable: Iterable[T]) -> bool:
    return sum(1 for item in iterable if pred(item)) >= n


def atmost[T](n: int, pred: Callable[[T], bool], iterable: Iterable[T]) -> bool:
    return sum(1 for item in iterable if pred(item)) <= n
```

Jeśli nie chcesz zużyć całego iteratora, możesz zrobić wersję z wcześniejszym wyjściem:

```python
def atleast_lazy[T](n: int, pred: Callable[[T], bool], iterable: Iterable[T]) -> bool:
    count = 0
    for item in iterable:
        if pred(item):
            count += 1
            if count >= n:
                return True
    return False
```

---

## Iterator

Iterator implementuje:

```python
class MyIterator:
    def __iter__(self):
        return self

    def __next__(self):
        ...
```

`for` woła pod spodem:

1. `iter(obj)`
2. wielokrotnie `next(...)`
3. kończy po `StopIteration`

### Przykład iteratora

```python
class CountDown:
    def __init__(self, start: int) -> None:
        self.current = start

    def __iter__(self) -> "CountDown":
        return self

    def __next__(self) -> int:
        if self.current < 0:
            raise StopIteration
        value = self.current
        self.current -= 1
        return value
```

---

## Generator

Generator to prostszy iterator z `yield`.

```python
def countdown(start: int):
    while start >= 0:
        yield start
        start -= 1
```

Użycie:

```python
gen = countdown(3)
print(next(gen))  # 3
print(next(gen))  # 2

for x in countdown(3):
    print(x)
```

### Generator expression

```python
squares = (x * x for x in range(10))
print(next(squares))  # 0
```

---

## Iterator haseł

```python
import random
import string


class PasswordGenerator:
    def __init__(
        self,
        length: int,
        charset: str = string.ascii_letters + string.digits,
        count: int = 10,
    ) -> None:
        self.length = length
        self.charset = charset
        self.count = count
        self.generated = 0

    def __iter__(self) -> "PasswordGenerator":
        return self

    def __next__(self) -> str:
        if self.generated >= self.count:
            raise StopIteration

        self.generated += 1
        return "".join(random.choice(self.charset) for _ in range(self.length))
```

---

## Domknięcie

Domknięcie to funkcja pamiętająca zmienne z zewnętrznego zakresu.

```python
def make_multiplier(n: int):
    def inner(x: int) -> int:
        return x * n

    return inner


times_3 = make_multiplier(3)
print(times_3(10))  # 30
```

### Generator budowany z funkcji

```python
from collections.abc import Callable, Iterator


def make_generator[T](func: Callable[[int], T]) -> Iterator[T]:
    n = 1
    while True:
        yield func(n)
        n += 1
```

Przykłady:

```python
arith = make_generator(lambda n: 2 * n + 1)
geom = make_generator(lambda n: 2 ** n)

print(next(arith))  # 3
print(next(arith))  # 5
print(next(geom))   # 2
```

---

## Memoizacja

Najprościej przez `functools.cache` albo `lru_cache`.

```python
from functools import cache, lru_cache


@cache
def fib(n: int) -> int:
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


@lru_cache(maxsize=128)
def catalan(n: int) -> int:
    if n == 0:
        return 1
    return sum(catalan(i) * catalan(n - 1 - i) for i in range(n))
```

### Memoizowany generator z funkcji

```python
from collections.abc import Callable, Iterator
from functools import cache


def make_generator_mem[T](func: Callable[[int], T]) -> Iterator[T]:
    cached = cache(func)
    n = 1
    while True:
        yield cached(n)
        n += 1
```

Jeśli `func` jest rekurencyjna, najczyściej dekorować ją bezpośrednio `@cache`.

---

## Dekoratory

Dekorator przyjmuje funkcję i zwraca nową funkcję.

```python
from collections.abc import Callable
from functools import wraps


def my_decorator(func: Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("przed")
        result = func(*args, **kwargs)
        print("po")
        return result

    return wrapper


@my_decorator
def hello(name: str) -> str:
    return f"Hello {name}"
```

`@wraps(func)` zachowuje nazwę i metadane oryginalnej funkcji.

---

## `logging`

Podstawy:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

logger = logging.getLogger(__name__)

logger.debug("debug")
logger.info("info")
logger.warning("warning")
logger.error("error")
```

Poziomy:

- `DEBUG`
- `INFO`
- `WARNING`
- `ERROR`
- `CRITICAL`

---

## Dekorator `log`

```python
import logging
import time
from collections.abc import Callable
from functools import wraps

logger = logging.getLogger(__name__)


def log(func: Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        logger.info("call %s args=%s kwargs=%s", func.__name__, args, kwargs)
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        logger.info("done %s result=%r time=%.6fs", func.__name__, result, elapsed)
        return result

    return wrapper
```

Wersja odporna na wyjątki:

```python
def log(func: Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            logger.info("call %s args=%s kwargs=%s", func.__name__, args, kwargs)
            result = func(*args, **kwargs)
            logger.info(
                "done %s result=%r time=%.6fs",
                func.__name__,
                result,
                time.perf_counter() - start,
            )
            return result
        except Exception:
            logger.exception("error in %s after %.6fs", func.__name__, time.perf_counter() - start)
            raise

    return wrapper
```

---

