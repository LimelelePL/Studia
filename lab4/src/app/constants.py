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


AUDIO_SUFFIXES = {".mp3", ".wav", ".flac", ".aac", ".ogg", "jp.m4a", ".wma"}
VIDEO_SUFFIXES = {".mp4", ".avi", ".mkv", ".mov", ".wmv", ".webm", ".flv", ".mpeg", ".mpg", ".m4v"}
IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff", ".webp", ".svg", ".ico"}
