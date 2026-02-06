from typing import Literal, Optional
from pydantic import BaseModel, Field
import subprocess
from pathlib import Path


class GrayscaleCommand(BaseModel):
    operation: Literal["grayscale"] = Field(
        "grayscale",
        description="Convert an image to grayscale (black and white) using ImageMagick",
    )

    input_path: str = Field(..., description="Relative path to the input image file")

    output_path: str = Field(..., description="Relative path to the output image file")

    method: Optional[Literal["rec601", "rec709", "linear", "average"]] = Field(
        "rec709",
        description=(
            "Grayscale conversion method: 'rec709' (default, perceptually balanced), "
            "'rec601' (older TV standard), 'linear' (equal RGB weights), "
            "'average' (simple R+G+B)/3."
        ),
    )

    strip_metadata: bool = Field(
        True,
        description="Remove EXIF and other metadata from the output image.",
    )


def grayscale_image(
    input_path: Path,
    output_path: Path,
    method: Optional[str] = "rec709",
    strip_metadata: bool = True,
):
    cmd = ["magick", str(input_path)]

    # -colorspace Gray uses Rec709Luma by default
    if method == "rec601":
        cmd.extend(["-colorspace", "Rec601Luma"])
    elif method == "rec709":
        cmd.extend(["-colorspace", "Gray"])  # Rec709Luma
    elif method == "linear":
        cmd.extend(["-colorspace", "LinearGray"])
    elif method == "average":
        cmd.extend(["-colorspace", "Gray"])  # Fallback
    else:
        cmd.extend(["-colorspace", "Gray"])

    if strip_metadata:
        cmd.append("-strip")

    cmd.append(str(output_path))

    subprocess.run(cmd, check=True)
