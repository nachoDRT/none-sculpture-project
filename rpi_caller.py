import requests
import cv2
import os
import tempfile

# api_url = "https://bacana-test-k6q6fewzaq-no.a.run.app/download-video/"
# api_url = "https://bacana-image-web-k6q6fewzaq-no.a.run.app/download-video/"
# api_url = "http://localhost:8080/download-video/"
api_url = "https://bacana-30-05-b-k6q6fewzaq-no.a.run.app/download-video/"
video_name = "latest.mp4"
url = api_url + video_name

save_here = os.path.join(os.getcwd(), "app", "client_store", video_name)

response = requests.get(api_url)

if response.status_code == 200:
    video_content = response.content

    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_file:
        temp_file.write(video_content)

    video_path = temp_file.name

    cap = cv2.VideoCapture(video_path)

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    break_flag = False
    while True:
        for frame_index in range(total_frames):
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
            ret, frame = cap.read()

            if not ret:
                break

            cv2.imshow("Video Bacano", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break_flag = True
                break

        if break_flag != True:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        else:
            break

    cap.release()
    cv2.destroyAllWindows()

else:
    print("\n Error downloading video:", response.text)
