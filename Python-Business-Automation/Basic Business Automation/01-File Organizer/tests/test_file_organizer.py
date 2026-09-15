from pathlib import Path
import sys
import pytest

# Allow pytest to import file_organizer.py from the src folder
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from file_organizer import (
    get_category,
    get_unique_destination,
    organize_files,
)


# Test 1
def test_get_category_image():
    """Test that image files are categorized correctly."""
    file_path = Path("photo.jpg")

    assert get_category(file_path) == "Images"


# Test 2
def test_get_category_document():
    """Test that document files are categorized correctly."""
    file_path = Path("notes.txt")

    assert get_category(file_path) == "Documents"


# Test 3
def test_get_category_pdf():
    """Test that PDF files are categorized correctly."""
    file_path = Path("invoice.pdf")

    assert get_category(file_path) == "PDFs"


# Test 4
def test_get_category_unknown_file():
    """Test that unknown files go into Other."""
    file_path = Path("unknown.xyz")

    assert get_category(file_path) == "Other"


# Test 5
def test_get_unique_destination():
    """Test that a unique filename is created."""
    destination = Path("report.txt")

    assert get_unique_destination(destination) == destination


# Test 6
def test_organize_files(tmp_path):
    """Test that files are moved into the correct category folders."""

    # Create sample files
    image_file = tmp_path / "photo.jpg"
    document_file = tmp_path / "notes.txt"
    pdf_file = tmp_path / "invoice.pdf"

    image_file.touch()
    document_file.touch()
    pdf_file.touch()

    results = organize_files(tmp_path)

    # Check results
    assert results["organized"] == 3
    assert results["errors"] == 0

    # Check files were moved
    assert (tmp_path / "Images" / "photo.jpg").exists()
    assert (tmp_path / "Documents" / "notes.txt").exists()
    assert (tmp_path / "PDFs" / "invoice.pdf").exists()


# Test 7
def test_organize_files_missing_directory():
    """Test that a missing directory raises FileNotFoundError."""

    missing_directory = Path("this_directory_does_not_exist")

    with pytest.raises(FileNotFoundError):
        organize_files(missing_directory)
