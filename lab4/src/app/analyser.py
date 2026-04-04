import json
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any


def read_dir_path() -> Path | None:
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


def calculate_stats(stats: list[dict[str, Any]]) -> dict[str, int | str]:
    total_chars = 0
    total_words = 0
    total_lines = 0
    char_counter: Counter[str] = Counter()
    word_counter: Counter[str] = Counter()

    for stat in stats:
        total_chars += int(stat["char count"])
        total_words += int(stat["word count"])
        total_lines += int(stat["lines count"])

        most_char = stat["most frequent char"]
        most_word = stat["most frequent word"]

        char_counter[most_char[0]] += most_char[1]
        word_counter[most_word[0]] += most_word[1]

    return {
        "files count": len(stats),
        "total char count": total_chars,
        "total word count": total_words,
        "total lines count": total_lines,
        "most frequent char": char_counter.most_common(1)[0][0],
        "most frequent word": word_counter.most_common(1)[0][0],
    }


def analyse() -> None | dict[str, int | str]:
    entry_path = read_dir_path()
    if not entry_path:
        return None

    files_in_dir = find_txt_files(entry_path)
    stats: list[dict[str, Any]] = []

    for file in files_in_dir:
        process_result = subprocess.run(
            ["python", "src/app/text_analyser.py"],
            input=f"{file}\n",
            text=True,
            capture_output=True,
        )
        if process_result.returncode != 0 or not process_result.stdout.strip():
            continue

        data = json.loads(process_result.stdout)
        stats.append(data)

    return calculate_stats(stats)


if __name__ == "__main__":
    if result := analyse():
        print(result)
