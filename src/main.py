# main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
from pathlib import Path

root_dir = Path(__file__).parent.parent
static_content_path = root_dir / "static"


app = FastAPI(title="Survey-Game API")
app.mount("/static", StaticFiles(directory=static_content_path), name="static")


@app.get("/", summary="Serve the homepage.")
def home():
    return FileResponse(static_content_path / "index.html")


@app.get("/hello", summary="A proof of concept API endpoint for debugging.")
def hello():
    return {"message": "Hello from FastAPI!"}


if __name__ == "__main__":
    uvicorn.run(app, port=8000)
