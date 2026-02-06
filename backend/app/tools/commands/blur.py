from typing import Literal, Optional
from pydantic import BaseModel, Field
import subprocess
from pathlib import Path


class BlurCommand(BaseModel):
    operation: Literal["blur"] = Field(
        "blur",
        description="Apply Gaussian blur to reduce noise or soften an image",
    )

    input_path: str = Field(..., description="Relative path to the input image file")

    output_path: str = Field(..., description="Relative path to the output image file")

    radius: float = Field(
        ...,
        ge=0,
        description=(
            "Blur radius in pixels. Controls the size of the convolution kernel. "
            "Use 0 to let ImageMagick auto-calculate from sigma. "
            "Typical values: 0-2 for subtle, 3-5 for moderate, 10+ for strong blur."
        ),
    )

    sigma: Optional[float] = Field(
        None,
        ge=0,
        description=(
            "Blur strength (standard deviation). This is the primary blur intensity. "
            "If omitted, defaults to radius or 1.0. Smaller values (0.5-2) for "
            "subtle softening, larger (5-15) for dramatic blur."
        ),
    )

    strip_metadata: bool = Field(
        True,
        description="Remove EXIF and other metadata from the output image.",
    )


def blur_image(
    input_path: Path,
    output_path: Path,
    radius: float,
    sigma: Optional[float] = None,
    strip_metadata: bool = True,
):
    cmd = ["magick", str(input_path)]

    # ImageMagick -blur: radius{xsigma}; if sigma omitted, radius is used for both
    if sigma is not None:
        blur_arg = f"{radius}x{sigma}"
    else:
        blur_arg = str(radius)

    cmd.extend(["-blur", blur_arg])

    if strip_metadata:
        cmd.append("-strip")

    cmd.append(str(output_path))

    subprocess.run(cmd, check=True)
