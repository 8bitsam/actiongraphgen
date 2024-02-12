### Database module to initialize and get files ###
### SOURCE: https://thepythoncode.com/article/using-google-drive--api-in-python ###


from __future__ import print_function

import os.path
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# If modifying these scopes, delete the file token.pickle.
SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly", "https://www.googleapis.com/auth/drive.file"]


def get_gdrive_service():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    # return Google Drive API service
    return build("drive", "v3", credentials=creds)


def get_size_format(b, factor=1024, suffix="B"):
    """
    Scale bytes to its proper byte format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if b < factor:
            return f"{b:.2f}{unit}{suffix}"
        b /= factor
    return f"{b:.2f}Y{suffix}"


def list_files(items):
    """given items returned by Google Drive API, prints them in a tabular way"""
    if not items:
        # empty drive
        print("No files found.")
    else:
        rows = []
        for item in items:
            # get the File ID
            id = item["id"]
            # get the name of file
            name = item["name"]
            try:
                # parent directory ID
                parents = item["parents"]
            except:
                # has no parrents
                parents = "N/A"
            try:
                # get the size in nice bytes format (KB, MB, etc.)
                size = get_size_format(int(item["size"]))
            except:
                # not a file, may be a folder
                size = "N/A"
            # get the Google Drive type of file
            mime_type = item["mimeType"]
            # get last modified date time
            modified_time = item["modifiedTime"]
            # append everything to the list
            rows.append((id, name, parents, size, mime_type, modified_time))
        print("Files:")
        # convert to a human readable table
        table = tabulate(rows, headers=["ID", "Name", "Parents", "Size", "Type", "Modified Time"])
        # print the table
        print(table)


def upload_files():
    """
    Creates a folder and upload a file to it
    """
    # authenticate account
    service = get_gdrive_service()
    # folder details we want to make
    folder_metadata = {"name": "TestFolder", "mimeType": "application/vnd.google-apps.folder"}
    # create the folder
    file = service.files().create(body=folder_metadata, fields="id").execute()
    # get the folder id
    folder_id = file.get("id")
    print("Folder ID:", folder_id)
    # upload a file text file
    # first, define file metadata, such as the name and the parent folder ID
    file_metadata = {"name": "test.txt", "parents": [folder_id]}
    # upload
    media = MediaFileUpload("test.txt", resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields="id").execute()
    print("File created, id:", file.get("id"))
