from typing import Literal, Optional
from pydantic import BaseModel, Field
import subprocess
from pathlib import Path


class ConvertFormatCommand(BaseModel):
    operation: Literal["convert"] = Field(
        "convert",
        description="Convert an image to a different file format using ImageMagick",
    )

    input_path: str = Field(..., description="Relative path to the input image file")

    output_path: str = Field(
        ...,
        description="Relative path to the output image file (extension determines format)",
    )

    format: Literal["png", "jpg", "jpeg", "webp", "avif", "gif", "bmp", "tiff"] = Field(
        ...,
        description=(
            "Target image format. PNG and WebP support transparency; "
            "JPEG is lossy and does not. Use 'webp' or 'avif' for modern web optimization."
        ),
    )

    quality: Optional[int] = Field(
        None,
        ge=1,
        le=100,
        description=(
            "Compression quality for lossy formats (JPEG, WebP, AVIF). "
            "Higher values mean better quality but larger files. "
            "Typical: 80-95 for JPEG, 80-90 for WebP. Ignored for lossless formats."
        ),
    )

    strip_metadata: bool = Field(
        True,
        description="Remove EXIF and other metadata from the output image.",
    )


def convert_image(
    input_path: Path,
    output_path: Path,
    format: str,
    quality: Optional[int] = None,
    strip_metadata: bool = True,
):
    cmd = ["magick", str(input_path)]

    if quality is not None:
        cmd.extend(["-quality", str(quality)])

    if strip_metadata:
        cmd.append("-strip")

    cmd.append(str(output_path))

    subprocess.run(cmd, check=True)
