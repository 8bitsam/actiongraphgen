import io
import json

import google.auth
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload


def fetch_and_print_json(file_name):
    # Load pre-authorized user credentials from the environment
    creds, _ = google.auth.default()

    # Create Drive API client
    service = build("drive", "v3", credentials=creds)

    # Get the file ID of the JSON file
    file_id = get_file_id(service, file_name)

    if file_id is None:
        print(f"Error: {file_name} does not exist in the Google Drive.")
        return

    # Download the JSON file
    request = service.files().get_media(fileId=file_id)
    downloaded_file = io.BytesIO()
    downloader = MediaIoBaseDownload(downloaded_file, request)
    done = False
    while done is False:
        _, done = downloader.next_chunk()

    # Load the JSON file and print it
    downloaded_file.seek(0)
    json_dict = json.load(downloaded_file)
    print(json_dict)


def get_file_id(service, file_name):
    # Get the list of files in the Google Drive
    results = service.files().list().execute()
    items = results.get("files", [])

    # Find the file with the specified name
    for item in items:
        if item["name"] == file_name:
            return item["id"]

    return None
