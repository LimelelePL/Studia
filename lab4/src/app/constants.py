from enum import Enum
from pathlib import Path
from typing import NamedTuple


class PathMode(str, Enum):
    ONLY_DIRS = "only_dirs"
    ALL = "all"


class TailParams(NamedTuple):
    lines: int = 10  # Domyślnie 10
    file_path: Path | None = None
    follow: bool = False
