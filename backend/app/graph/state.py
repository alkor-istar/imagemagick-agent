from pydantic import BaseModel
from typing import Optional, List
from app.tools.commands import ImageCommand


class ImageMetadata(BaseModel):
    width: int
    height: int
    format: str
    mode: Optional[str] = None


class PlanStep(BaseModel):
    operation: str
    reason: str


class ImageAgentState(BaseModel):
    image_metadata: ImageMetadata
    user_request: str
    current_input_path: str

    plan: Optional[List[PlanStep]] = None
    current_step_index: int = 0

    current_command: Optional[ImageCommand] = None
    current_output_path: Optional[str] = None

    error: Optional[str] = None
