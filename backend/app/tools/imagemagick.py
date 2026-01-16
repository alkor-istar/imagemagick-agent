import subprocess
from pathlib import Path


def resize_image(input_path: Path, output_path: Path, width: int, height: int):
    print("input_path:", input_path)
    print("output_path:", output_path)
    print("width:", width)
    print("height:", height)
    cmd = [
        "magick",
        input_path,
        "-resize",
        f"{width}x{height}",
        output_path,
    ]

    print("After cmd", cmd)

    subprocess.run(cmd, check=True)

    print("After subprocess run")
