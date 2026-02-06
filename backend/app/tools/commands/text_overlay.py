from typing import Literal, Optional
from pydantic import BaseModel, Field
import subprocess
from pathlib import Path


class TextOverlayCommand(BaseModel):
    operation: Literal["text_overlay"] = Field(
        "text_overlay",
        description="Draw text onto an image at a specified position",
    )

    input_path: str = Field(..., description="Relative path to the input image file")

    output_path: str = Field(..., description="Relative path to the output image file")

    text: str = Field(
        ...,
        description="The text string to draw on the image. Supports UTF-8.",
    )

    x: int = Field(
        ...,
        description="Horizontal position in pixels from the left edge (or from gravity anchor).",
    )

    y: int = Field(
        ...,
        description="Vertical position in pixels from the top edge (or from gravity anchor).",
    )

    font_size: int = Field(
        24,
        gt=0,
        le=512,
        description="Font size in points. Typical: 12-72 for body text, 24-48 for overlays.",
    )

    color: str = Field(
        "white",
        description=(
            "Text color. Use named colors ('white', 'black', 'red') or "
            "hex values ('#FFFFFF', '#000000')."
        ),
    )

    gravity: Optional[
        Literal[
            "northwest",
            "north",
            "northeast",
            "west",
            "center",
            "east",
            "southwest",
            "south",
            "southeast",
        ]
    ] = Field(
        None,
        description=(
            "Anchor point for text positioning. If set, x and y are offsets "
            "from this anchor (e.g. 'south' + y=10 places text 10px above bottom)."
        ),
    )

    stroke_color: Optional[str] = Field(
        None,
        description="Outline/stroke color for text. Improves readability on busy backgrounds.",
    )

    stroke_width: Optional[int] = Field(
        None,
        ge=0,
        le=20,
        description="Width of text outline in pixels. Use with stroke_color for legibility.",
    )

    strip_metadata: bool = Field(
        True,
        description="Remove EXIF and other metadata from the output image.",
    )


def text_overlay(
    input_path: Path,
    output_path: Path,
    text: str,
    x: int,
    y: int,
    font_size: int = 24,
    color: str = "white",
    gravity: Optional[str] = None,
    stroke_color: Optional[str] = None,
    stroke_width: Optional[int] = None,
    strip_metadata: bool = True,
):
    cmd = ["magick", str(input_path)]

    if gravity:
        cmd.extend(["-gravity", gravity])

    cmd.extend(["-pointsize", str(font_size)])
    cmd.extend(["-fill", color])

    if stroke_color is not None and stroke_width is not None and stroke_width > 0:
        cmd.extend(["-stroke", stroke_color])
        cmd.extend(["-strokewidth", str(stroke_width)])

    # -annotate uses +x+y for offset (relative to gravity)
    cmd.extend(["-annotate", f"+{x}+{y}", text])

    if strip_metadata:
        cmd.append("-strip")

    cmd.append(str(output_path))

    subprocess.run(cmd, check=True)
