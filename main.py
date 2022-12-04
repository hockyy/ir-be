import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from generator import generate_bsbi
from model import ErrorResponse, SearchQuery, SearchResponse, \
  engine_to_result_list, DocsQuery, get_content, SpellCheckResponse

load_dotenv()
app = FastAPI()
STATIC_PATH = "/static"
BSBI_instance = None

origins = [
  "*"
]


@app.on_event("startup")
async def startup_event():
  global BSBI_instance
  BSBI_instance = generate_bsbi()


app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["POST", "GET"],
  allow_headers=["*"],
)


@app.get("/")
async def read_root():
  return {
    "code": 200
  }


@app.post("/search", response_model=SearchResponse)
async def search(query: SearchQuery):
  result = BSBI_instance.retrieve_bm25(query.content, k=query.k, optimize=True)
  result = engine_to_result_list(result)
  return SearchResponse(200, result)


@app.post("/spellcheck", response_model=SpellCheckResponse)
async def search(query: SearchQuery):
  result, changed = BSBI_instance.spellcheck(query.content)
  return SpellCheckResponse(200, result, changed)


@app.post("/collection")
async def read_root(query: DocsQuery):
  return {
    "content": get_content(query.part, query.cid)
  }


def common_error(err: Exception):
  """
  Returns abnormal JSONResponse
  """
  return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                      content=ErrorResponse("invalid request",
                                            f"{str(err)}").dict())


if __name__ == "__main__":
  uvicorn.run("main:app", host="0.0.0.0", port=8080, log_level="info")
