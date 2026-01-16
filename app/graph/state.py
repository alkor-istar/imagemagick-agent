from pydantic import BaseModel
from typing import Optional


class ImageAgentState(BaseModel):
    user_request: str
    plan: Optional[str] = None
    command: Optional[dict] = None
    result_path: Optional[str] = None
    error: Optional[str] = None
