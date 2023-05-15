import requests
import os


def upload_video(name, url):
    with open(name, "rb") as file:
        server_response = requests.post(url=url, files={"video": file})

    return server_response


def get_video(url):
    server_response = requests.get(url=url)

    return server_response


def save_downloaded_video(video):
    if not os.path.exists("flask_local_test/client"):
        os.makedirs("flask_local_test/client")

    with open("flask_local_test/client/video.mp4", "wb") as f:
        f.write(video)


if __name__ == "__main__":
    base_url = "http://localhost:8000"

    video_name = os.path.join(os.getcwd(), "res", "test_video.mp4")

    if upload_video(name=video_name, url=base_url + "/upload").status_code != 200:
        print("WARNING: Problems while uploading video")

    else:
        server_response = get_video(url=base_url + "/server_videos/test_video.mp4")

        if server_response.status_code != 200:
            print("WARNING: Problems while downloading video")

        else:
            save_downloaded_video(video=server_response.content)
