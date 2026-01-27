from PIL import Image
from pathlib import Path
from app.graph.state import ImageMetadata


def extract_metadata(image_path: Path) -> ImageMetadata:
    with Image.open(image_path) as img:
        return ImageMetadata(
            width=img.width,
            height=img.height,
            format=img.format,
            mode=img.mode,
        )
