from typing import Literal, Optional
from pydantic import BaseModel, Field
import subprocess
from pathlib import Path


class ResizeCommand(BaseModel):
    operation: Literal["resize"] = Field(
        "resize", description="Resize an image using ImageMagick resize operation"
    )

    input_path: str = Field(..., description="Relative path to the input image file")

    output_path: str = Field(..., description="Relative path to the output image file")

    width: int = Field(..., gt=0, le=4096, description="Target width in pixels")

    height: int = Field(..., gt=0, le=4096, description="Target height in pixels")

    keep_aspect_ratio: bool = Field(
        True,
        description=(
            "Preserve the original aspect ratio. "
            "If false, the image may be distorted to exactly match width and height."
        ),
    )

    resize_mode: Optional[Literal["shrink", "enlarge", "exact", "cover"]] = Field(
        None,
        description=(
            "Controls how resizing is applied:\n"
            "- 'shrink': only resize if the image is larger than the target (>)\n"
            "- 'enlarge': only resize if the image is smaller than the target (<)\n"
            "- 'exact': force exact dimensions, ignoring aspect ratio (!)\n"
            "- 'cover': fill the target dimensions and crop excess (^)"
        ),
    )

    filter: Optional[
        Literal[
            "nearest",
            "box",
            "triangle",
            "hermite",
            "hanning",
            "hamming",
            "blackman",
            "gaussian",
            "quadratic",
            "cubic",
            "catrom",
            "mitchell",
            "lanczos",
        ]
    ] = Field(
        None,
        description=(
            "Resampling filter used during resize. "
            "Lanczos is high quality for downscaling; "
            "nearest is fast but low quality."
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
            "Anchor point used when cropping or extending the image. "
            "Commonly used with 'cover' mode or when padding."
        ),
    )

    background: Optional[str] = Field(
        None,
        description=(
            "Background color used when padding the image "
            "(e.g. 'white', 'black', 'transparent')."
        ),
    )

    quality: Optional[int] = Field(
        None,
        ge=1,
        le=100,
        description=(
            "Compression quality for lossy output formats like JPEG or WEBP. "
            "Ignored for lossless formats."
        ),
    )

    sharpen: Optional[float] = Field(
        None,
        ge=0.0,
        description=(
            "Apply unsharp mask after resizing to improve perceived sharpness. "
            "Typical values range from 0.5 to 1.5."
        ),
    )

    strip_metadata: bool = Field(
        True,
        description=(
            "Remove EXIF and other metadata from the output image to reduce file size."
        ),
    )


def resize_image(
    input_path: Path,
    output_path: Path,
    width: int,
    height: int,
    keep_aspect_ratio: bool = True,
    resize_mode: Optional[str] = None,
    filter: Optional[str] = None,
    gravity: Optional[str] = "center",
    background: Optional[str] = None,
    quality: Optional[int] = None,
    sharpen: Optional[float] = None,
    strip_metadata: bool = True,
):
    cmd = ["magick", str(input_path)]

    # Resampling filter
    if filter:
        cmd.extend(["-filter", filter])

    # Build resize geometry
    geometry = f"{width}x{height}"

    if resize_mode == "shrink":
        geometry += ">"
    elif resize_mode == "enlarge":
        geometry += "<"
    elif resize_mode == "exact":
        geometry += "!"
    elif resize_mode == "cover":
        geometry += "^"

    if not keep_aspect_ratio and resize_mode is None:
        geometry += "!"

    cmd.extend(["-resize", geometry])

    # Handle cover mode cropping
    if resize_mode == "cover":
        cmd.extend(["-gravity", gravity or "center", "-extent", f"{width}x{height}"])

    # Background for padding or transparency
    if background:
        cmd.extend(["-background", background])

    # Sharpen after resize (common best practice)
    if sharpen is not None:
        cmd.extend(["-unsharp", f"0x{sharpen}"])

    # Strip metadata
    if strip_metadata:
        cmd.append("-strip")

    # Output quality
    if quality is not None:
        cmd.extend(["-quality", str(quality)])

    cmd.append(str(output_path))

    subprocess.run(cmd, check=True)
