import subprocess
from pathlib import Path


def resize_image(input_path: Path, output_path: Path, width: int, height: int):
    cmd = [
        "magick",
        input_path,
        "-resize",
        f"{width}x{height}",
        output_path,
    ]

    subprocess.run(cmd, check=True)


def convert_image(input_path: Path, output_path: Path, format: str):
    cmd = [
        "magick",
        input_path,
        output_path,
    ]

    subprocess.run(cmd, check=True)


def crop_image(
    input_path: Path, output_path: Path, x: int, y: int, width: int, height: int
):
    cmd = [
        "magick",
        input_path,
        "-crop",
        f"{width}x{height}+{x}+{y}",
        output_path,
    ]

    subprocess.run(cmd, check=True)


def rotate_image(input_path: Path, output_path: Path, degrees: int):
    cmd = [
        "magick",
        input_path,
        "-rotate",
        f"{degrees}",
        output_path,
    ]

    subprocess.run(cmd, check=True)


def flip_image(input_path: Path, output_path: Path, direction: str):
    cmd = [
        "magick",
        input_path,
        "-flip",
        direction,
        output_path,
    ]

    subprocess.run(cmd, check=True)


def quality_image(input_path: Path, output_path: Path, quality: int):
    cmd = [
        "magick",
        input_path,
        "-quality",
        f"{quality}",
        output_path,
    ]

    subprocess.run(cmd, check=True)


def grayscale_image(input_path: Path, output_path: Path):
    cmd = [
        "magick",
        input_path,
        "-colorspace",
        "gray",
        output_path,
    ]

    subprocess.run(cmd, check=True)


def brightness_contrast_image(
    input_path: Path, output_path: Path, brightness: int, contrast: int
):
    cmd = [
        "magick",
        input_path,
        "-brightness-contrast",
        f"{brightness}x{contrast}",
        output_path,
    ]

    subprocess.run(cmd, check=True)


def blur_image(input_path: Path, output_path: Path, radius: float):
    cmd = [
        "magick",
        input_path,
        "-blur",
        f"{radius}",
        output_path,
    ]

    subprocess.run(cmd, check=True)


def text_overlay(
    input_path: Path,
    output_path: Path,
    text: str,
    x: int,
    y: int,
    font_size: int,
    color: str,
):
    cmd = [
        "magick",
        input_path,
        "-pointsize",
        f"{font_size}",
        "-fill",
        f"{color}",
        "-annotate",
        f"+{x}+{y}",
        f"{text}",
        output_path,
    ]

    subprocess.run(cmd, check=True)
