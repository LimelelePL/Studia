import subprocess

from constants import AUDIO_SUFFIXES, IMAGE_SUFFIXES, VIDEO_SUFFIXES
from utils import (
    append_history_to_file,
    build_output_name,
    find_media_files,
    get_output_dir,
    is_audio_file,
    is_image_file,
    is_video_file,
    read_media_converts_args,
    write_history,
)


def convert_files():
    path, format = read_media_converts_args()
    media_files = find_media_files(path)
    program: str = ""
    converted = False
    output_suffix = format

    for f in media_files:
        output_name = build_output_name(f.stem, format)
        output_path = get_output_dir() / output_name
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if is_audio_file(f) or is_video_file(f):
            if output_suffix not in AUDIO_SUFFIXES.union(VIDEO_SUFFIXES):
                continue
            subprocess.run(["ffmpeg", "-y", "-i", str(f), str(output_path)], check=True)
            program = "ffmpeg"
            converted = True
        elif is_image_file(f):
            if output_suffix not in IMAGE_SUFFIXES:
                continue
            subprocess.run(["magick", str(f), str(output_path)], check=True)
            program = "magick"
            converted = True
        else:
            continue
        history = write_history(str(f), format, str(output_path), program)
        if converted:
            append_history_to_file(get_output_dir(), history)


if __name__ == "__main__":
    convert_files()
