import io
import json

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload


def fetch_and_print_json(file_name):
    # Load pre-authorized user credentials from the environment
    creds, _ = google.auth.default()

    # Create Drive API client
    service = build("drive", "v3", credentials=creds)

    try:
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
    except HttpError as e:
        print(f"HTTP Error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        # Clean up resources
        if "downloaded_file" in locals():
            downloaded_file.close()


def get_file_id(service, file_name):
    # Search for the file with the specified name
    results = service.files().list(q=f"name='{file_name}'").execute()
    items = results.get("files", [])

    if items:
        return items[0]["id"]
    else:
        return None


# Example usage
if __name__ == "__main__":
    fetch_and_print_json("your_file.json")
