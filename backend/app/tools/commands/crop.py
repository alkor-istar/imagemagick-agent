from typing import Literal, Optional
from pydantic import BaseModel, Field
import subprocess
from pathlib import Path


class CropCommand(BaseModel):
    operation: Literal["crop"] = Field(
        "crop", description="Crop a rectangular region from an image"
    )

    input_path: str = Field(..., description="Relative path to the input image file")

    output_path: str = Field(..., description="Relative path to the output image file")

    width: int = Field(
        ..., gt=0, le=4096, description="Width of the cropped region in pixels"
    )

    height: int = Field(
        ..., gt=0, le=4096, description="Height of the cropped region in pixels"
    )

    x_offset: Optional[int] = Field(
        None,
        ge=0,
        description=(
            "Horizontal offset in pixels from the left edge. "
            "If omitted, gravity will be used."
        ),
    )

    y_offset: Optional[int] = Field(
        None,
        ge=0,
        description=(
            "Vertical offset in pixels from the top edge. "
            "If omitted, gravity will be used."
        ),
    )

    gravity: Optional[
        Literal[
            "north",
            "south",
            "east",
            "west",
            "center",
            "northwest",
            "northeast",
            "southwest",
            "southeast",
        ]
    ] = Field(
        "center",
        description=(
            "Anchor point used to position the crop area when offsets are not provided. "
            "Defaults to center cropping."
        ),
    )

    repage: bool = Field(
        True,
        description=(
            "Remove the virtual canvas metadata after cropping (+repage). "
            "Recommended to avoid unexpected offsets in downstream operations."
        ),
    )

    strip_metadata: bool = Field(
        True, description=("Remove EXIF and other metadata from the output image.")
    )


def crop_image(
    input_path: Path,
    output_path: Path,
    width: int,
    height: int,
    x_offset: Optional[int] = None,
    y_offset: Optional[int] = None,
    gravity: Optional[str] = "center",
    repage: bool = True,
    strip_metadata: bool = True,
):
    cmd = ["magick", str(input_path)]

    # Use gravity if explicit offsets are not provided
    if x_offset is None or y_offset is None:
        cmd.extend(["-gravity", gravity or "center"])

    # Build crop geometry
    if x_offset is not None and y_offset is not None:
        geometry = f"{width}x{height}+{x_offset}+{y_offset}"
    else:
        geometry = f"{width}x{height}"

    cmd.extend(["-crop", geometry])

    # Remove virtual canvas metadata
    if repage:
        cmd.append("+repage")

    # Strip metadata
    if strip_metadata:
        cmd.append("-strip")

    cmd.append(str(output_path))

    subprocess.run(cmd, check=True)
