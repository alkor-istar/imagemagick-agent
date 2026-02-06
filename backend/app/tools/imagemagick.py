import subprocess
from pathlib import Path

from app.tools.commands import (
    blur_image,
    brightness_contrast_image,
    convert_image,
    crop_image,
    flip_image,
    grayscale_image,
    quality_image,
    resize_image,
    rotate_image,
    text_overlay,
)


def _run_crop(c):
    return crop_image(
        Path(c.input_path),
        Path(c.output_path),
        width=c.width,
        height=c.height,
        x_offset=getattr(c, "x_offset", None),
        y_offset=getattr(c, "y_offset", None),
        gravity=getattr(c, "gravity", "center"),
        repage=getattr(c, "repage", True),
        strip_metadata=getattr(c, "strip_metadata", True),
    )


def _run_resize(c):
    return resize_image(
        Path(c.input_path),
        Path(c.output_path),
        width=c.width,
        height=c.height,
        keep_aspect_ratio=getattr(c, "keep_aspect_ratio", True),
        resize_mode=getattr(c, "resize_mode", None),
        filter=getattr(c, "filter", None),
        gravity=getattr(c, "gravity", "center"),
        background=getattr(c, "background", None),
        quality=getattr(c, "quality", None),
        sharpen=getattr(c, "sharpen", None),
        strip_metadata=getattr(c, "strip_metadata", True),
    )


def _run_convert(c):
    return convert_image(
        Path(c.input_path),
        Path(c.output_path),
        format=c.format,
        quality=getattr(c, "quality", None),
        strip_metadata=getattr(c, "strip_metadata", True),
    )


def _run_rotate(c):
    return rotate_image(
        Path(c.input_path),
        Path(c.output_path),
        degrees=c.degrees,
        background=getattr(c, "background", "white"),
        strip_metadata=getattr(c, "strip_metadata", True),
    )


def _run_flip(c):
    return flip_image(
        Path(c.input_path),
        Path(c.output_path),
        direction=c.direction,
        strip_metadata=getattr(c, "strip_metadata", True),
    )


def _run_quality(c):
    return quality_image(
        Path(c.input_path),
        Path(c.output_path),
        quality=c.quality,
        strip_metadata=getattr(c, "strip_metadata", True),
    )


def _run_grayscale(c):
    return grayscale_image(
        Path(c.input_path),
        Path(c.output_path),
        method=getattr(c, "method", "rec709"),
        strip_metadata=getattr(c, "strip_metadata", True),
    )


def _run_brightness_contrast(c):
    return brightness_contrast_image(
        Path(c.input_path),
        Path(c.output_path),
        brightness=c.brightness,
        contrast=c.contrast,
        strip_metadata=getattr(c, "strip_metadata", True),
    )


def _run_blur(c):
    return blur_image(
        Path(c.input_path),
        Path(c.output_path),
        radius=c.radius,
        sigma=getattr(c, "sigma", None),
        strip_metadata=getattr(c, "strip_metadata", True),
    )


def _run_text_overlay(c):
    return text_overlay(
        Path(c.input_path),
        Path(c.output_path),
        text=c.text,
        x=c.x,
        y=c.y,
        font_size=getattr(c, "font_size", 24),
        color=getattr(c, "color", "white"),
        gravity=getattr(c, "gravity", None),
        stroke_color=getattr(c, "stroke_color", None),
        stroke_width=getattr(c, "stroke_width", None),
        strip_metadata=getattr(c, "strip_metadata", True),
    )


COMMAND_EXECUTORS = {
    "blur": _run_blur,
    "brightness_contrast": _run_brightness_contrast,
    "convert": _run_convert,
    "crop": _run_crop,
    "flip": _run_flip,
    "grayscale": _run_grayscale,
    "quality": _run_quality,
    "resize": _run_resize,
    "rotate": _run_rotate,
    "text_overlay": _run_text_overlay,
}


def run_imagemagick(command):
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
