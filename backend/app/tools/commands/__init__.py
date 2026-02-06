"""ImageMagick command models and executors."""

from typing import Union

from app.tools.commands.blur import BlurCommand, blur_image
from app.tools.commands.brightness_contrast import (
    BrightnessContrastCommand,
    brightness_contrast_image,
)
from app.tools.commands.convert import ConvertFormatCommand, convert_image
from app.tools.commands.crop import CropCommand, crop_image
from app.tools.commands.flip import FlipCommand, flip_image
from app.tools.commands.grayscale import GrayscaleCommand, grayscale_image
from app.tools.commands.quality import QualityCommand, quality_image
from app.tools.commands.resize import ResizeCommand, resize_image
from app.tools.commands.rotate import RotateCommand, rotate_image
from app.tools.commands.text_overlay import TextOverlayCommand, text_overlay

ImageCommand = Union[
    BlurCommand,
    BrightnessContrastCommand,
    ConvertFormatCommand,
    CropCommand,
    FlipCommand,
    GrayscaleCommand,
    QualityCommand,
    ResizeCommand,
    RotateCommand,
    TextOverlayCommand,
]

COMMAND_REGISTRY = {
    "blur": BlurCommand,
    "brightness_contrast": BrightnessContrastCommand,
    "convert": ConvertFormatCommand,
    "crop": CropCommand,
    "flip": FlipCommand,
    "grayscale": GrayscaleCommand,
    "quality": QualityCommand,
    "resize": ResizeCommand,
    "rotate": RotateCommand,
    "text_overlay": TextOverlayCommand,
}

__all__ = [
    "BlurCommand",
    "BrightnessContrastCommand",
    "COMMAND_REGISTRY",
    "ConvertFormatCommand",
    "CropCommand",
    "FlipCommand",
    "GrayscaleCommand",
    "ImageCommand",
    "QualityCommand",
    "ResizeCommand",
    "RotateCommand",
    "TextOverlayCommand",
    "blur_image",
    "brightness_contrast_image",
    "convert_image",
    "crop_image",
    "flip_image",
    "grayscale_image",
    "quality_image",
    "resize_image",
    "rotate_image",
    "text_overlay",
]
