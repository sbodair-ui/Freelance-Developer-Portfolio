from pathlib import Path
import sys

import pandas as pd
import pytest


# Add the src folder to Python's import path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_DIRECTORY = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_DIRECTORY))


from invoice_processor import (
    validate_required_columns,
    identify_invalid_records,
    separate_valid_and_invalid_records,
    calculate_line_totals,
    calculate_invoice_summary,
    calculate_processing_summary,
    generate_output_files,
)


def create_test_dataframe():
    """Create sample invoice data for testing."""

    return pd.DataFrame(
        {
            "Invoice ID": [
                "INV-001",
                "INV-001",
                "INV-002",
                "INV-003",
            ],
            "Customer": [
                "Acme Company",
                "Acme Company",
                "Smith Consulting",
                None,
            ],
            "Product": [
                "Laptop",
                "Mouse",
                "Monitor",
                "Desk",
            ],
            "Quantity": [
                2,
                5,
                2,
                1,
            ],
            "Unit Price": [
                1000.00,
                25.00,
                250.00,
                350.00,
            ],
        }
    )


def test_validate_required_columns():
    """Test that valid invoice data passes validation."""

    dataframe = create_test_dataframe()

    validate_required_columns(dataframe)


def test_validate_required_columns_missing_column():
    """Test that missing columns raise ValueError."""

    dataframe = pd.DataFrame(
        {
            "Invoice ID": ["INV-001"],
            "Customer": ["Acme Company"],
        }
    )

    with pytest.raises(ValueError):
        validate_required_columns(dataframe)


def test_identify_invalid_records():
    """Test that invalid records are identified correctly."""

    dataframe = create_test_dataframe()

    invalid_records = identify_invalid_records(dataframe)

    assert invalid_records.sum() == 1


def test_separate_valid_and_invalid_records():
    """Test that valid and invalid records are separated."""

    dataframe = create_test_dataframe()

    valid_records, invalid_records = (
        separate_valid_and_invalid_records(dataframe)
    )

    assert len(valid_records) == 3
    assert len(invalid_records) == 1


def test_calculate_line_totals():
    """Test line total calculations."""

    dataframe = create_test_dataframe()

    valid_records, _ = (
        separate_valid_and_invalid_records(dataframe)
    )

    result = calculate_line_totals(valid_records)

    assert result["Line Total"].tolist() == [
        2000.00,
        125.00,
        500.00,
    ]


def test_calculate_invoice_summary():
    """Test invoice total calculations."""

    dataframe = create_test_dataframe()

    valid_records, _ = (
        separate_valid_and_invalid_records(dataframe)
    )

    valid_records = calculate_line_totals(valid_records)

    result = calculate_invoice_summary(valid_records)

    invoice_001 = result[
        result["Invoice ID"] == "INV-001"
    ].iloc[0]

    assert invoice_001["Invoice_Total"] == 2125.00
    assert invoice_001["Line_Items"] == 2


def test_calculate_processing_summary():
    """Test processing summary calculations."""

    dataframe = create_test_dataframe()

    valid_records, invalid_records = (
        separate_valid_and_invalid_records(dataframe)
    )

    valid_records = calculate_line_totals(valid_records)

    invoice_summary = calculate_invoice_summary(
        valid_records
    )

    summary = calculate_processing_summary(
        valid_records,
        invalid_records,
        invoice_summary,
    )

    assert summary["Total Records Processed"] == 4
    assert summary["Valid Records"] == 3
    assert summary["Invalid Records"] == 1
    assert summary["Invoices Processed"] == 2
    assert summary["Total Invoice Value"] == 2625.00


def test_generate_output_files(tmp_path):
    """Test that all output files are generated."""

    dataframe = create_test_dataframe()

    valid_records, invalid_records = (
        separate_valid_and_invalid_records(dataframe)
    )

    valid_records = calculate_line_totals(valid_records)

    invoice_summary = calculate_invoice_summary(
        valid_records
    )

    processing_summary = calculate_processing_summary(
        valid_records,
        invalid_records,
        invoice_summary,
    )

    generate_output_files(
        valid_records,
        invalid_records,
        invoice_summary,
        processing_summary,
        tmp_path,
    )

    assert (
        tmp_path / "processed_invoices.csv"
    ).exists()

    assert (
        tmp_path / "invalid_records.csv"
    ).exists()

    assert (
        tmp_path / "invoice_summary.csv"
    ).exists()

    assert (
        tmp_path / "processing_summary.txt"
    ).exists()
