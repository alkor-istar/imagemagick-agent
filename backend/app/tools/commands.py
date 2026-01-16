from pydantic import BaseModel, Field
from typing import Literal, Union


class ResizeCommand(BaseModel):
    operation: Literal["resize"]
    input_path: str = Field(..., description="Relative path to input image")
    output_path: str = Field(..., description="Relative path to output image")
    width: int = Field(..., gt=0, le=4096)
    height: int = Field(..., gt=0, le=4096)


ImageCommand = Union[ResizeCommand]
