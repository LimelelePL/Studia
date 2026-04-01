from enum import Enum
from pathlib import Path
from typing import Final, NamedTuple


class PathMode(str, Enum):
    ONLY_DIRS = "only_dirs"
    ALL = "all"


class TailConstants:
    LINES_PREFIX: Final = "--lines="
    DEFAULT_LINES: Final = 10


class TailParams(NamedTuple):
    lines: int = 10  # Domyślnie 10
    file_path: Path | None = None
    follow: bool = False
