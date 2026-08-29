from pathlib import Path
import sys

import pytest


# Add the src folder to Python's import path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_DIRECTORY = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_DIRECTORY))


from file_organizer import (
    get_category,
    get_unique_destination,
    organize_files,
)


def test_get_category_for_image():
    """Test that image files are categorized correctly."""

    file_path = Path("photo.jpg")

    assert get_category(file_path) == "Images"


def test_get_category_for_pdf():
    """Test that PDF files are categorized correctly."""

    file_path = Path("invoice.pdf")

    assert get_category(file_path) == "PDFs"


def test_get_category_for_excel():
    """Test that Excel files are categorized correctly."""

    file_path = Path("report.xlsx")

    assert get_category(file_path) == "Excel"


def test_get_category_for_unknown_file():
    """Test that unknown file types go into Other."""

    file_path = Path("unknown.xyz")

    assert get_category(file_path) == "Other"


def test_get_unique_destination_when_file_does_not_exist(tmp_path):
    """Test that the original destination is returned when available."""

    destination = tmp_path / "report.pdf"

    result = get_unique_destination(destination)

    assert result == destination


def test_get_unique_destination_when_file_exists(tmp_path):
    """Test that a unique filename is created."""

    destination = tmp_path / "report.pdf"

    destination.touch()

    result = get_unique_destination(destination)

    assert result.name == "report_1.pdf"


def test_organize_files(tmp_path):
    """Test that files are moved into the correct directories."""

    # Create test files
    (tmp_path / "photo.jpg").touch()
    (tmp_path / "invoice.pdf").touch()
    (tmp_path / "notes.txt").touch()
    (tmp_path / "unknown.xyz").touch()

    results = organize_files(tmp_path)

    # Check results
    assert results["organized"] == 4
    assert results["errors"] == 0

    # Check files were moved
    assert (tmp_path / "Images" / "photo.jpg").exists()
    assert (tmp_path / "PDFs" / "invoice.pdf").exists()
    assert (tmp_path / "Documents" / "notes.txt").exists()
    assert (tmp_path / "Other" / "unknown.xyz").exists()


def test_organize_files_missing_directory():
    """Test that a missing directory raises FileNotFoundError."""

    missing_directory = Path("this_directory_does_not_exist")

    with pytest.raises(FileNotFoundError):
        organize_files(missing_directory)
