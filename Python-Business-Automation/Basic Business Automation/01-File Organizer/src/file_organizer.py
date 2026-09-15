from pathlib import Path
import shutil
import logging


FILE_CATEGORIES = {
    "Images": {
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
        ".bmp",
        ".svg",
        ".webp",
    },
    "Documents": {
        ".txt",
        ".doc",
        ".docx",
        ".odt",
        ".rtf",
    },
    "Excel": {
        ".xls",
        ".xlsx",
        ".xlsm",
        ".csv",
    },
    "PDFs": {
        ".pdf",
    },
    "Presentations": {
        ".ppt",
        ".pptx",
        ".odp",
    },
    "Videos": {
        ".mp4",
        ".mov",
        ".avi",
        ".mkv",
        ".wmv",
    },
    "Audio": {
        ".mp3",
        ".wav",
        ".flac",
        ".aac",
        ".ogg",
    },
    "Archives": {
        ".zip",
        ".rar",
        ".7z",
        ".tar",
        ".gz",
    },
}


logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
)


def get_category(file_path: Path) -> str:
    """Return the category for a file based on its extension."""

    extension = file_path.suffix.lower()

    for category, extensions in FILE_CATEGORIES.items():
        if extension in extensions:
            return category

    return "Other"


def get_unique_destination(destination: Path) -> Path:
    """Create a unique filename if the destination already exists."""

    if not destination.exists():
        return destination

    counter = 1

    while True:
        new_name = (
            f"{destination.stem}_{counter}"
            f"{destination.suffix}"
        )

        new_destination = destination.with_name(new_name)

        if not new_destination.exists():
            return new_destination

        counter += 1


def organize_files(source_directory: Path) -> dict:
    """Organize files in the source directory."""

    if not source_directory.exists():
        raise FileNotFoundError(
            f"Directory does not exist: {source_directory}"
        )

    if not source_directory.is_dir():
        raise NotADirectoryError(
            f"Path is not a directory: {source_directory}"
        )

    results = {
        "organized": 0,
        "skipped": 0,
        "errors": 0,
    }

    for file_path in source_directory.iterdir():

        if not file_path.is_file():
            continue

        try:
            category = get_category(file_path)

            category_directory = source_directory / category
            category_directory.mkdir(
                parents=True,
                exist_ok=True,
            )

            destination = category_directory / file_path.name
            destination = get_unique_destination(destination)

            shutil.move(
                str(file_path),
                str(destination),
            )

            logging.info(
                "Moved: %s -> %s",
                file_path.name,
                category,
            )

            results["organized"] += 1

        except Exception as error:
            logging.error(
                "Could not organize %s: %s",
                file_path.name,
                error,
            )

            results["errors"] += 1

    return results


def main() -> None:
    """Run the file organizer."""

    print("File Organizer")
    print("-" * 40)

    directory_input = input(
        "Enter the directory to organize: "
    ).strip()

    source_directory = Path(directory_input)

    try:
        results = organize_files(source_directory)

        print("\nOrganization complete!")
        print(f"Files organized: {results['organized']}")
        print(f"Files skipped: {results['skipped']}")
        print(f"Errors: {results['errors']}")

    except (FileNotFoundError, NotADirectoryError) as error:
        print(f"\nError: {error}")


if __name__ == "__main__":
    main()
