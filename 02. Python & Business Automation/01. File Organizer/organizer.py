
from pathlib import Path


def get_files(folder_path):
    """
    Retrieve all files from a specified folder.
    """

    folder = Path(folder_path)

    files = []

    for item in folder.iterdir():
        if item.is_file():
            files.append(item)

    return files


