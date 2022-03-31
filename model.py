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


class ErrorResponse(BaseModel):
    def __init__(self, error: str, error_description: str, **data: Any):
        super().__init__(**data)
        self.error = error
        self.error_description = error_description

    error: str = "invalid_token"
    error_description: str = "An error has occured"
