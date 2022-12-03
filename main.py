import io
import json

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse, StreamingResponse

import generator
from model import ErrorResponse

load_dotenv()
app = FastAPI()
STATIC_PATH = "/static"

origins = [
    "*"
]

@app.on_event("startup")
async def startup_event():
    # await generator.init()
    pass

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

def common_error(err: Exception):
    """
    Returns abnormal JSONResponse
    """
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                        content=ErrorResponse("invalid request", f"{str(err)}").dict())


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, log_level="info")