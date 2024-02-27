from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.responses import FileResponse
import os

app = FastAPI()

def get_latest_preview():
    try:
        with open("preview.txt", "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return ""



@app.get("/", response_class=HTMLResponse)
async def index():
    return FileResponse('templates/index.html')
@app.get("/get-preview")
async def get_preview():
    content = get_latest_preview()
    return JSONResponse({"content": content})