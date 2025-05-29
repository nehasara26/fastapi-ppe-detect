from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import FileResponse, RedirectResponse
import shutil
import os
from inference import run_inference
import logging

app = FastAPI()

UPLOAD_DIR = "uploads"
OUTPUT_PATH = "static/output.mp4"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs("static", exist_ok=True)

@app.post("/upload/")
async def upload_video(file: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Run inference
    run_inference(file_location, OUTPUT_PATH)

    return FileResponse(OUTPUT_PATH, media_type="video/mp4", filename="ppe_output.mp4")


@app.get("/")
def redirect_to_docs():
    return RedirectResponse(url="/docs")

# On startup, dynamically print Swagger UI URL
@app.on_event("startup")
async def startup_event():
    import socket
    host = socket.gethostbyname(socket.gethostname())
    logging.info(f"🚀 Swagger UI available at: http://{host}:8000/docs")

#uvicorn main:app --reload