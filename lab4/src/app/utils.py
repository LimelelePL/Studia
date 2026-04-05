import sys
from pathlib import Path

from app.constants import AUDIO_SUFFIXES, IMAGE_SUFFIXES, VIDEO_SUFFIXES


def read_dir_path_from_cli() -> Path | None:
    if len(sys.argv) < 2:
        return None

    arg = Path(sys.argv[1])
    if not arg.is_dir():
        return None

    return arg


def find_txt_files(dir_path: Path) -> set[Path]:
    result: set[Path] = set()
    for file in dir_path.iterdir():
        if file.is_file() and file.suffix == ".txt":
            result.add(file)
    return result


def is_audio_file(file: Path) -> bool:
    return file.is_file() and file.suffix.lower() in AUDIO_SUFFIXES


def is_video_file(file: Path) -> bool:
    return file.is_file() and file.suffix.lower() in VIDEO_SUFFIXES


def is_image_file(file: Path) -> bool:
    return file.is_file() and file.suffix.lower() in IMAGE_SUFFIXES


def find_media_files(dir_path: Path) -> set[Path]:
    result: set[Path] = set()
    for file in dir_path.iterdir():
        if is_audio_file(file) or is_video_file(file) or is_image_file(file):
            result.add(file)
    return result
