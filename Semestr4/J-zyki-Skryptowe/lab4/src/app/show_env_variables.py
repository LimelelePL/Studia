import os
import sys
from collections.abc import Iterable


def filter_env_variables(env_items: list[tuple[str, str]], filters: list[str]) -> list[tuple[str, str]]:

    if not filters:
        return env_items

    lowered_filters = [f.casefold() for f in filters]
    filtered: list[tuple[str, str]] = []

    for name, value in env_items:
        name_lower = name.casefold()
        for filter in lowered_filters:
            if filter in name_lower:
                filtered.append((name, value))
                break

    return filtered


def sorted_env_variables(env_variables: list[tuple[str, str]]) -> list[tuple[str, str]]:
    return sorted(env_variables, key=lambda item: item[0].casefold())


def print_env_variables(env_variables: Iterable[tuple[str, str]]) -> None:
    for name, value in env_variables:
        print(f"{name}={value}")


def show_env_variables() -> None:
    cli_args = list(filter(None, sys.argv[1:]))
    env_variables = list(os.environ.items())
    env_variables = filter_env_variables(env_variables, cli_args)
    print_env_variables(sorted_env_variables(env_variables))


if __name__ == "__main__":
    show_env_variables()
