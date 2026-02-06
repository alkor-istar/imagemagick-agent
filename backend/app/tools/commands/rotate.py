from typing import Literal, Optional
from pydantic import BaseModel, Field
import subprocess
from pathlib import Path


class RotateCommand(BaseModel):
    operation: Literal["rotate"] = Field(
        "rotate",
        description="Rotate an image by a specified angle using ImageMagick",
    )

    input_path: str = Field(..., description="Relative path to the input image file")

    output_path: str = Field(..., description="Relative path to the output image file")

    degrees: float = Field(
        ...,
        ge=-360,
        le=360,
        description=(
            "Rotation angle in degrees. Positive values rotate clockwise. "
            "Use 90, 180, or 270 for common right-angle rotations."
        ),
    )

    background: Optional[str] = Field(
        "white",
        description=(
            "Color for areas revealed when the rotated image extends beyond "
            "the original canvas. Use 'transparent' for PNG output, or "
            "named colors like 'white', 'black', or hex values."
        ),
    )

    strip_metadata: bool = Field(
        True,
        description="Remove EXIF and other metadata from the output image.",
    )


def rotate_image(
    input_path: Path,
    output_path: Path,
    degrees: float,
    background: Optional[str] = "white",
    strip_metadata: bool = True,
):
    cmd = ["magick", str(input_path)]

    if background:
        cmd.extend(["-background", background])

    cmd.extend(["-rotate", str(degrees)])

    if strip_metadata:
        cmd.append("-strip")

    cmd.append(str(output_path))

    subprocess.run(cmd, check=True)
