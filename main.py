from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

import generator
import os

from model import GenshinQuery, GenshinResponse

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


@app.post("/genshin", response_model=GenshinResponse)
async def read_genshin(genshinQuery: GenshinQuery):
    url = STATIC_PATH + "/" + await generator.generateAchievement(genshinQuery.caption, genshinQuery.language)
    return GenshinResponse(url, "Image succesfully generated", 200)
