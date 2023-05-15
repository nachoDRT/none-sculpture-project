import requests
import cv2
import os


def play_video():
    print(os.path.join(os.getcwd(), "app", "raspberry_pi", "bacana.mp4"))
    cap = cv2.VideoCapture(
        os.path.join(os.getcwd(), "app", "raspberry_pi", "bacana.mp4")
    )

    # Verify if the video is loaded
    if not cap.isOpened():
        print("Error trying to play video")
        exit()

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        cv2.imshow("Bacana", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


api_url = "http://localhost:8000/download-video/"

video_name = "test_video.mp4"

response = requests.get(api_url + video_name)


if response.status_code == 200:
    video_content = response.json()["video_content"]
    play_video()


else:
    print("\n Error downloading video:", response.text)
