from fastapi import FastAPI, File, UploadFile, HTTPException
from google.cloud import storage
import uvicorn
import os
import io

# Imports needed to have the HTML interface
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, StreamingResponse, FileResponse


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
    with open(index_path) as file:
        return file.read()


@app.get("{file_path:path}", include_in_schema=False)
async def serve_static_file(file_path: str):
    static_path = file_path
    print("hola", static_path)

    if os.path.isfile(static_path) and "static" in file_path:
        media_type = (
            "text/css" if file_path.endswith(".css") else "application/javascript"
        )
        return FileResponse(static_path, media_type=media_type)

    raise HTTPException(status_code=404)


@app.post("/upload-video/")
async def upload_video(file: UploadFile = File(...)):
    filename = "latest.mp4"
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

    video_buffer = io.BytesIO()
    blob.download_to_file(video_buffer)
    video_buffer.seek(0)

    headers = {
        "Content-Disposition": f"attachment; filename={video_name}",
        "Content-Type": "video/mp4",
    }

    return StreamingResponse(video_buffer, headers=headers)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080)
