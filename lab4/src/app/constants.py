from enum import StrEnum
from pathlib import Path
from typing import NamedTuple


class PathMode(StrEnum):
    DIR = "dir"
    ALL = "all"


class TailParams(NamedTuple):
    lines: int = 10
    file_path: Path | None = None
    follow: bool = False
