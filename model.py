from typing import Any, Optional
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List


class SearchQuery(BaseModel):
  content: str
  k: Optional[int] = 10
  rerank: Optional[bool]


class Result(BaseModel):
  def __init__(self, score: int, path: str, **data: Any):
    super().__init__(**data)
    self.score = score
    self.path = path
    self.id = path.split('/')[-1]
    with(open(path, "r")) as buffer:
      tmp_buffer = buffer.read()
      self.excerpt = (tmp_buffer[:min(len(tmp_buffer), 50)])

  path: Optional[str] = ""
  score: Optional[int] = 0
  id: Optional[str] = ""
  excerpt: Optional[str] = ""

class SearchResponse(BaseModel):
  def __init__(self, code: int, results: List[Result], **data: Any):
    super().__init__(**data)
    self.code = code
    self.results = results

  results: Optional[List[Result]] = []
  code: Optional[int] = 500

def engine_to_result_list(engine_list):
  result_list = [Result(engine_result[0], engine_result[1]) for engine_result in engine_list]
  return result_list

class ErrorResponse(BaseModel):
  def __init__(self, error: str, error_description: str, **data: Any):
    super().__init__(**data)
    self.error = error
    self.error_description = error_description

  error: str = "invalid_token"
  error_description: str = "An error has occured"
