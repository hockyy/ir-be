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
import os
import redis

load_dotenv()
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT"))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
EXPIRE_IMAGE = 60

image_db = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)

db_dict = {
    "image_db" : image_db
}

from model import GenshinQuery, GenshinResponse, ErrorResponse

app = FastAPI()
try:
    os.makedirs('output')
except:
    pass
STATIC_PATH = "/static"
app.mount(STATIC_PATH, StaticFiles(directory="output"), name="static")

origins = [
    "http://genshin.hocky.id",
    "https://genshin.hocky.id",
    "http://localhost:3000",
    "https://genshin-achievements-frontend.vercel.app"
]

@app.on_event("startup")
async def startup_event():
    await generator.init()

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


@app.get("/check_db")
async def check_db():
    """
    Print all values in redis database
    """
    all_values = dict()
    for db_name, redis_db in db_dict.items():
        tmp_dict = dict()
        redis_keys = redis_db.keys()
        for redis_key in redis_keys:
            redis_value = redis_db.get(redis_key)
            try:
                redis_string = redis_value.decode("utf-8")
            except:
                redis_string = redis_value.hex()
            if(not redis_string.startswith("{")):
                redis_string = f"\"{redis_string}\""
            print(redis_string)
            tmp_dict[redis_key] = json.loads(redis_string)
        all_values[db_name] = tmp_dict
    return all_values

@app.post("/genshin", response_model=GenshinResponse)
async def read_genshin(genshinQuery: GenshinQuery):
    url, image = await generator.generateAchievement(genshinQuery.caption, genshinQuery.language)
    image_db.set(url, image,ex=EXPIRE_IMAGE)
    return GenshinResponse(f"/image/{url}", "Image succesfully generated", 200)

@app.get("/image/{image_url}")
async def read_image(image_url:str):
    try:
        data = image_db.get(image_url)
        return StreamingResponse(io.BytesIO(data), media_type="image/png")
    except Exception as e:
        return common_error(e)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, log_level="info")