from typing import Literal
from pydantic import BaseModel, Field
import subprocess
from pathlib import Path


class FlipCommand(BaseModel):
    operation: Literal["flip"] = Field(
        "flip",
        description="Mirror an image horizontally or vertically using ImageMagick",
    )

    input_path: str = Field(..., description="Relative path to the input image file")

    output_path: str = Field(..., description="Relative path to the output image file")

    direction: Literal["horizontal", "vertical"] = Field(
        ...,
        description=(
            "Mirror direction: 'horizontal' flips left-to-right (like a mirror), "
            "'vertical' flips top-to-bottom."
        ),
    )

    strip_metadata: bool = Field(
        True,
        description="Remove EXIF and other metadata from the output image.",
    )


def flip_image(
    input_path: Path,
    output_path: Path,
    direction: str,
    strip_metadata: bool = True,
):
    cmd = ["magick", str(input_path)]

    # ImageMagick: -flip = vertical (top-to-bottom), -flop = horizontal (left-to-right)
    if direction == "vertical":
        cmd.append("-flip")
    else:
        cmd.append("-flop")

    if strip_metadata:
        cmd.append("-strip")

    cmd.append(str(output_path))

    subprocess.run(cmd, check=True)
