import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

from constants import AUDIO_SUFFIXES, IMAGE_SUFFIXES, VIDEO_SUFFIXES


def read_media_converts_args() -> tuple[Path, str]:
    parser = argparse.ArgumentParser()

    parser.add_argument("dir", type=Path)
    parser.add_argument("format", type=str)

    allowed_suffixes = [suffix for suffix in AUDIO_SUFFIXES.union(IMAGE_SUFFIXES).union(VIDEO_SUFFIXES)]
    args = parser.parse_args()

    if not Path(args.dir).is_dir():
        raise NotADirectoryError(f"Ścieżka '{args.dir}' nie jest katalogiem!")
    if args.format.lower() not in allowed_suffixes:
        raise ValueError(f"Rozszerzenie pliku '{args.format}' jest niedozwolone!")

    return args.dir, args.format.lower()


def write_history(source_path: str, output_format: str, output_path: str, program: str) -> dict[str, str]:
    now = datetime.now()
    history_timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

    return {
        "timestamp": history_timestamp,
        "source_path": source_path,
        "output_format": output_format,
        "output_path": output_path,
        "program": program,
    }


def append_history_to_file(output_dir: Path, history: dict[str, str]) -> None:
    dir_path = Path(output_dir)
    dir_path.mkdir(parents=True, exist_ok=True)
    file_path = dir_path / "history.json"

    if file_path.exists():
        with open(file_path, encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = []

    data.append(history)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def get_output_dir() -> Path:
    if converted_dir := os.environ.get("CONVERTED_DIR"):
        return Path(converted_dir)
    return Path.cwd() / "converted"


def build_output_name(source_name: str, output_format: str) -> str:
    timestamp = datetime.now().strftime("%Y%m%d")
    return f"{timestamp}-{source_name}{output_format}"


def find_txt_files(dir_path: Path) -> set[Path]:
    result: set[Path] = set()
    for file in dir_path.iterdir():
        if file.is_file() and file.suffix == ".txt":
            result.add(file)
    return result


def read_cli_dir():
    res = Path(sys.argv[1])

    if not res.is_dir():
        raise NotADirectoryError(f"Ścieżka '{res}' nie jest katalogiem!")

    return res


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
