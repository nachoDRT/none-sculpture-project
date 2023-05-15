from google.cloud import storage
import os


BUCKET = "none-sculpture-project"
BLOB = "video_1"


def upload_to_google_cloud(
    credential_path: str, video_path: str, bucket_name: str, blob_name: str
):
    storage_client = storage.Client.from_service_account_json(credential_path)
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(video_path)
    print(
        f"The file {video_path} has been successfully uploaded to {blob_name} in the bucket {bucket_name}."
    )


def download_from_google_cloud(
    credential_path: str, bucket_name: str, file_name: str, storing_path: str
):
    client = storage.Client.from_service_account_json(credential_path)
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(file_name)
    blob.download_to_filename(storing_path)


if __name__ == "__main__":
    credentials = os.path.join(os.getcwd(), "credentials", "credentials.json")
    save_here = os.path.join(os.getcwd(), "app", "client_gcloud", "downloaded.mp4")

    # download_from_google_cloud(
    #     credential_path=credentials,
    #     bucket_name=BUCKET,
    #     file_name="video_1",
    #     storing_path=save_here,
    # )

    video = os.path.join(os.getcwd(), "res", "test_video.mp4")
    upload_to_google_cloud(
        credential_path=credentials,
        video_path=video,
        bucket_name=BUCKET,
        blob_name=BLOB,
    )
