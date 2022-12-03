from typing import Any, Optional
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List


class SearchQuery(BaseModel):
  content: str
  rerank: Optional[bool]


class Result(BaseModel):
  def __init__(self, code: int, **data: Any):
    super().__init__(**data)
    self.code = code

  score: Optional[int] = 0
  id: Optional[str] = ""
  excerpt: Optional[str] = ""


class SearchResponse(BaseModel):
  def __init__(self, code: int, **data: Any):
    super().__init__(**data)
    self.code = code

  results: Optional[List[Result]] = []
  code: Optional[int] = 500


class ErrorResponse(BaseModel):
  def __init__(self, error: str, error_description: str, **data: Any):
    super().__init__(**data)
    self.error = error
    self.error_description = error_description

  error: str = "invalid_token"
  error_description: str = "An error has occured"
