from flask import Flask, send_from_directory, render_template
import os

server = Flask(__name__)


@server.route("/")
def index():
    return render_template("upload_video.html")


if __name__ == "__main__":
    server.run(debug=True, port=8000)
