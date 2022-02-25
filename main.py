from typing import Optional

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

import generator
from model import GenshinQuery, GenshinResponse

app = FastAPI()
STATIC_PATH = "/static"
app.mount(STATIC_PATH, StaticFiles(directory="output"), name="static")

@app.get("/")
def read_root():
    return {
        "code": 200
    }

@app.post("/genshin", response_model=GenshinResponse)
def read_genshin(genshinQuery : GenshinQuery):
    url = STATIC_PATH + "/" + generator.init(genshinQuery.caption)
    return GenshinResponse(url, "Image succesfully generated", 200)