from pydantic import BaseModel, Field
from typing import Literal, Union


class ResizeCommand(BaseModel):
    operation: Literal["resize"]
    input_path: str = Field(..., description="Relative path to input image")
    output_path: str = Field(..., description="Relative path to output image")
    width: int = Field(..., gt=0, le=4096)
    height: int = Field(..., gt=0, le=4096)


class CropCommand(BaseModel):
    operation: Literal["crop"]
    input_path: str
    output_path: str
    x: int = Field(..., ge=0)
    y: int = Field(..., ge=0)
    width: int = Field(..., gt=0, le=4096)
    height: int = Field(..., gt=0, le=4096)


class RotateCommand(BaseModel):
    operation: Literal["rotate"]
    input_path: str
    output_path: str
    degrees: float = Field(..., ge=-360, le=360)


class FlipCommand(BaseModel):
    operation: Literal["flip"]
    input_path: str
    output_path: str
    direction: Literal["horizontal", "vertical"]


class ConvertFormatCommand(BaseModel):
    operation: Literal["convert"]
    input_path: str
    output_path: str
    format: Literal["png", "jpg", "webp", "avif"]


class QualityCommand(BaseModel):
    operation: Literal["quality"]
    input_path: str
    output_path: str
    quality: int = Field(..., ge=1, le=100)


class GrayscaleCommand(BaseModel):
    operation: Literal["grayscale"]
    input_path: str
    output_path: str


class BrightnessContrastCommand(BaseModel):
    operation: Literal["brightness_contrast"]
    input_path: str
    output_path: str
    brightness: int = Field(..., ge=-100, le=100)
    contrast: int = Field(..., ge=-100, le=100)


class BlurCommand(BaseModel):
    operation: Literal["blur"]
    input_path: str
    output_path: str
    radius: float = Field(..., ge=0)


class TextOverlayCommand(BaseModel):
    operation: Literal["text_overlay"]
    input_path: str
    output_path: str
    text: str
    x: int
    y: int
    font_size: int = Field(..., gt=0, le=256)
    color: str = "white"


ImageCommand = Union[
    ResizeCommand,
    CropCommand,
    RotateCommand,
    FlipCommand,
    ConvertFormatCommand,
    QualityCommand,
    GrayscaleCommand,
    BrightnessContrastCommand,
    BlurCommand,
    TextOverlayCommand,
]

COMMAND_REGISTRY = {
    "resize": ResizeCommand,
    "crop": CropCommand,
    "rotate": RotateCommand,
    "flip": FlipCommand,
    "convert": ConvertFormatCommand,
    "quality": QualityCommand,
    "grayscale": GrayscaleCommand,
    "brightness_contrast": BrightnessContrastCommand,
    "blur": BlurCommand,
    "text_overlay": TextOverlayCommand,
}
