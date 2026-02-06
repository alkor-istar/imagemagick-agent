from typing import Literal
from pydantic import BaseModel, Field
import subprocess
from pathlib import Path


class BrightnessContrastCommand(BaseModel):
    operation: Literal["brightness_contrast"] = Field(
        "brightness_contrast",
        description="Adjust brightness and contrast of an image using ImageMagick",
    )

    input_path: str = Field(..., description="Relative path to the input image file")

    output_path: str = Field(..., description="Relative path to the output image file")

    brightness: int = Field(
        ...,
        ge=-100,
        le=100,
        description=(
            "Brightness adjustment (-100 to +100). Zero means no change. "
            "Positive values lighten, negative values darken the image."
        ),
    )

    contrast: int = Field(
        ...,
        ge=-100,
        le=100,
        description=(
            "Contrast adjustment (-100 to +100). Zero means no change. "
            "Positive values increase contrast (deeper blacks, brighter whites), "
            "negative values reduce it."
        ),
    )

    strip_metadata: bool = Field(
        True,
        description="Remove EXIF and other metadata from the output image.",
    )


def brightness_contrast_image(
    input_path: Path,
    output_path: Path,
    brightness: int,
    contrast: int,
    strip_metadata: bool = True,
):
    cmd = [
        "magick",
        str(input_path),
        "-brightness-contrast",
        f"{brightness}x{contrast}",
    ]

    if strip_metadata:
        cmd.append("-strip")

    cmd.append(str(output_path))

    subprocess.run(cmd, check=True)
