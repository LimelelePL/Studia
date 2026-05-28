# MODYFIKACJA 1
def count_calls(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.calls += 1  # type: ignore
        return func(*args, **kwargs)

    wrapper.calls = 0  # type: ignore
    return wrapper


# MODYFIKACJA 2
def call_once(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not wrapper.called:  # type: ignore
            wrapper.called = True  # type: ignore
            return func(*args, **kwargs)
        return None

    return wrapper
