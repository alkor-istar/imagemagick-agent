import subprocess
from pathlib import Path
from typing import Callable, Dict, Type


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
    print("In grayscale image: ", input_path, output_path)
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


COMMAND_EXECUTORS: Dict[str, Callable] = {
    "resize": lambda c: resize_image(
        Path(c.input_path),
        Path(c.output_path),
        c.width,
        c.height,
    ),
    "convert": lambda c: convert_image(
        Path(c.input_path),
        Path(c.output_path),
        c.format,
    ),
    "crop": lambda c: crop_image(
        Path(c.input_path),
        Path(c.output_path),
        c.x,
        c.y,
        c.width,
        c.height,
    ),
    "rotate": lambda c: rotate_image(
        Path(c.input_path),
        Path(c.output_path),
        c.degrees,
    ),
    "flip": lambda c: flip_image(
        Path(c.input_path),
        Path(c.output_path),
        c.direction,
    ),
    "quality": lambda c: quality_image(
        Path(c.input_path),
        Path(c.output_path),
        c.quality,
    ),
    "grayscale": lambda c: grayscale_image(
        Path(c.input_path),
        Path(c.output_path),
    ),
    "brightness_contrast": lambda c: brightness_contrast_image(
        Path(c.input_path),
        Path(c.output_path),
        c.brightness,
        c.contrast,
    ),
    "blur": lambda c: blur_image(
        Path(c.input_path),
        Path(c.output_path),
        c.radius,
    ),
    "text_overlay": lambda c: text_overlay(
        Path(c.input_path),
        Path(c.output_path),
        c.text,
        c.x,
        c.y,
        c.font_size,
        c.color,
    ),
}


def run_imagemagick(command):
    print("Run imagemagick", command)
    operation = command.operation

    if operation not in COMMAND_EXECUTORS:
        raise ValueError(f"Unsupported ImageMagick operation: {operation}")

    try:
        result = COMMAND_EXECUTORS[operation](command)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(
            f"ImageMagick failed for operation '{operation}': {e}"
        ) from e

    return result or command.output_path
