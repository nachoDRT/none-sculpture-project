from fastapi import FastAPI, File, UploadFile
from google.cloud import storage
import uvicorn
import os

# Imports needed to have the HTML interface
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse


app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Configure Google Cloud Storage client
credential_path = os.path.join(os.getcwd(), "app", "credentials", "credentials.json")
client = storage.Client.from_service_account_json(credential_path)
bucket_name = "none-sculpture-project"

# Path in bucket
videos_folder = "bacana_videos/"


@app.get("/", response_class=HTMLResponse)
async def read_index():
    index_path = os.path.join(os.getcwd(), "app", "static", "index.html")
    print(index_path)
    with open(index_path) as file:
        return file.read()


@app.post("/upload-video/")
async def upload_video(file: UploadFile = File(...)):
    filename = file.filename
    file_content = await file.read()

    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(videos_folder + filename)
    blob.upload_from_string(file_content)

    return {"message": "Vídeo subido correctamente"}


@app.get("/download-video/{video_name}")
async def download_video(video_name: str):
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(videos_folder + video_name)

    if not blob.exists():
        return {"message": "El vídeo no existe"}

    with open(
        os.path.join(os.getcwd(), "app", "client_store", "bacana.mp4"), "wb"
    ) as file:
        video_content = blob.download_to_file(file)

    return {"video_content": video_content}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080)
