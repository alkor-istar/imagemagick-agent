from typing import Literal, Optional
from pydantic import BaseModel, Field
import subprocess
from pathlib import Path


class QualityCommand(BaseModel):
    operation: Literal["quality"] = Field(
        "quality",
        description="Adjust compression quality of an image without changing format",
    )

    input_path: str = Field(..., description="Relative path to the input image file")

    output_path: str = Field(..., description="Relative path to the output image file")

    quality: int = Field(
        ...,
        ge=1,
        le=100,
        description=(
            "Compression quality level (1-100). Higher values preserve more detail "
            "but produce larger files. For JPEG: 85-95 is high quality, 70-80 for web. "
            "Only affects lossy formats (JPEG, WebP, etc.); ignored for PNG."
        ),
    )

    strip_metadata: bool = Field(
        True,
        description="Remove EXIF and other metadata from the output image.",
    )


def quality_image(
    input_path: Path,
    output_path: Path,
    quality: int,
    strip_metadata: bool = True,
):
    cmd = ["magick", str(input_path), "-quality", str(quality)]

    if strip_metadata:
        cmd.append("-strip")

    cmd.append(str(output_path))

    subprocess.run(cmd, check=True)
