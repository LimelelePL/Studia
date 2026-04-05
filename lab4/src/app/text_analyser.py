import json
import sys
from collections import Counter
from pathlib import Path


def read_txt_file_path() -> Path | None:
    raw_path = sys.stdin.readline().strip()
    if not raw_path:
        return None

    path = Path(raw_path)
    if not path.is_file() or path.suffix != ".txt":
        return None
    return path


def stats(path: Path) -> str | None:
    lines_count = 0
    char_counter: Counter[str] = Counter()
    word_counter: Counter[str] = Counter()

    with open(path) as f:
        for line in f:
            lines_count += 1
            for char in line:
                char_counter[char] += 1
            for word in line.split():
                word_counter[word] += 1

    stats = {
        "path": str(path),
        "char count": char_counter.total(),
        "word count": word_counter.total(),
        "lines count": lines_count,
        "most frequent char": list(char_counter.most_common(1)[0]) if char_counter else ["", 0],
        "most frequent word": list(word_counter.most_common(1)[0]) if word_counter else ["", 0],
    }

    return json.dumps(stats, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    path = read_txt_file_path()
    if path:
        result = stats(path)
        if result:
            sys.stdout.write(result)
