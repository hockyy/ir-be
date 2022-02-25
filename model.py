from typing import Any, Optional
from fastapi.responses import JSONResponse
from pydantic import BaseModel

class GenshinQuery(BaseModel):
    caption: str
    language: str

class GenshinResponse(BaseModel):
    def __init__(self, url: str, detail: str, code: int, **data: Any):
        super().__init__(**data)
        self.url = url
        self.detail = detail
        self.code = code
    url: Optional[str] = None
    detail: Optional[str] = None
    code: Optional[int] = 500