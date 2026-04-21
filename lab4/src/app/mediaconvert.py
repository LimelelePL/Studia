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
    source_directory, output_suffix = read_media_converts_args()
    media_files = find_media_files(source_directory)
    program: str = ""
    converted = False

    for input_file in media_files:
        output_name = build_output_name(f.stem, output_suffix)
        output_path = get_output_dir() / output_name
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # zeby 2 razy tego samego pliku nie konwertowac
        if output_path.exists():
            continue

        if (
            is_audio_file(input_file)
            and is_video_file(input_file)
            and output_suffix in AUDIO_SUFFIXES.union(VIDEO_SUFFIXES)
        ):
            subprocess.run(["ffmpeg", "-y", "-i", str(input_file), str(output_path)], check=True)
            program = "ffmpeg"
            converted = True
        elif is_image_file(f) and output_suffix in IMAGE_SUFFIXES:
            subprocess.run(["magick", str(input_file), str(output_path)], check=True)
            program = "magick"
            converted = True
        else:
            continue
        history = write_history(str(input), output_suffix, str(output_path), program)
        if converted:
            append_history_to_file(get_output_dir(), history)


if __name__ == "__main__":
    convert_files()
