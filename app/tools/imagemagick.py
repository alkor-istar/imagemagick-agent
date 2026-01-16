import subprocess
from pathlib import Path


def resize_image(input_path: Path, output_path: Path, width: int, height: int):
    cmd = ["magick", str(input_path), "-resize", f"{width}x{height}", str(output_path)]
    subprocess.run(cmd, check=True)
