from flask import Flask, send_from_directory, render_template, request
import os
from werkzeug.utils import secure_filename

server = Flask(__name__)
server.config["UPLOAD_FOLDER"] = "videos"

if not os.path.exists(server.config["UPLOAD_FOLDER"]):
    os.makedirs(server.config["UPLOAD_FOLDER"])


@server.route("/")
def index():
    return render_template("upload_video.html")


@server.route("/upload", methods=["POST"])
def upload():
    video = request.files["video"]
    video.save(
        os.path.join(server.config["UPLOAD_FOLDER"], secure_filename(video.filename))
    )
    return "Video was uploaded"


if __name__ == "__main__":
    server.run(debug=True, port=8000)
