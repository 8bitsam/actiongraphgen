from database import *


def init_drive():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 5 files the user has access to.
    """
    service = get_gdrive_service()
    # Call the Drive v3 API
    results = (
        service.files()
        .list(pageSize=5, fields="nextPageToken, files(id, name, mimeType, size, parents, modifiedTime)")
        .execute()
    )
    # get the results
    items = results.get("files", [])
    # list all 20 files & folders
    list_files(items)


def main():
    init_drive()


if __name__ == "__main__":
    main()
