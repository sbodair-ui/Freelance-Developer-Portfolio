from pathlib import Path
import sys

import pandas as pd
import pytest


# Add the src folder to Python's import path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_DIRECTORY = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_DIRECTORY))


from email_report import (
    load_business_data,
    validate_business_data,
    calculate_business_metrics,
    analyze_department_performance,
    generate_report,
    create_email,
    save_email,
)


def create_test_dataframe():
    """Create sample business data for testing."""

    return pd.DataFrame(
        {
            "Date": [
                "2026-01-01",
                "2026-01-02",
                "2026-01-03",
                "2026-01-04",
            ],
            "Department": [
                "Sales",
                "Marketing",
                "Sales",
                "Operations",
            ],
            "Revenue": [
                10000.00,
                5000.00,
                7500.00,
                4000.00,
            ],
            "Expenses": [
                4000.00,
                2000.00,
                2500.00,
                1500.00,
            ],
        }
    )


def test_validate_business_data():
    """Test that valid business data passes validation."""

    dataframe = create_test_dataframe()

    validate_business_data(dataframe)


def test_validate_business_data_missing_column():
    """Test that missing required columns raise ValueError."""

    dataframe = pd.DataFrame(
        {
            "Date": ["2026-01-01"],
            "Department": ["Sales"],
            "Revenue": [10000.00],
        }
    )

    with pytest.raises(ValueError):
        validate_business_data(dataframe)


def test_calculate_business_metrics():
    """Test business metric calculations."""

    dataframe = create_test_dataframe()

    metrics = calculate_business_metrics(
        dataframe
    )

    assert metrics["Total Revenue"] == 26500.00
    assert metrics["Total Expenses"] == 10000.00
    assert metrics["Net Revenue"] == 16500.00
    assert metrics["Average Revenue"] == 6625.00


def test_analyze_department_performance():
    """Test department performance calculations."""

    dataframe = create_test_dataframe()

    result = analyze_department_performance(
        dataframe
    )

    sales = result[
        result["Department"] == "Sales"
    ].iloc[0]

    assert sales["Total_Revenue"] == 17500.00
    assert sales["Total_Expenses"] == 6500.00
    assert sales["Net_Revenue"] == 11000.00


def test_generate_report(tmp_path):
    """Test business report generation."""

    dataframe = create_test_dataframe()

    metrics = calculate_business_metrics(
        dataframe
    )

    department_performance = (
        analyze_department_performance(
            dataframe
        )
    )

    output_file = (
        tmp_path / "business_report.txt"
    )

    generate_report(
        dataframe,
        metrics,
        department_performance,
        output_file,
    )

    assert output_file.exists()

    report_contents = (
        output_file.read_text(
            encoding="utf-8"
        )
    )

    assert (
        "BUSINESS PERFORMANCE REPORT"
        in report_contents
    )

    assert (
        "Total Revenue: $26,500.00"
        in report_contents
    )

    assert (
        "Total Expenses: $10,000.00"
        in report_contents
    )

    assert (
        "Net Revenue: $16,500.00"
        in report_contents
    )


def test_create_email(tmp_path):
    """Test email creation and attachment."""

    attachment = (
        tmp_path / "business_report.txt"
    )

    attachment.write_text(
        "Business Report",
        encoding="utf-8",
    )

    message = create_email(
        sender="automation@example.com",
        recipient="manager@example.com",
        subject="Business Performance Report",
        body="Attached is the business report.",
        attachment_path=attachment,
    )

    assert (
        message["From"]
        == "automation@example.com"
    )

    assert (
        message["To"]
        == "manager@example.com"
    )

    assert (
        message["Subject"]
        == "Business Performance Report"
    )

    assert (
        "Attached is the business report."
        in message.get_body().get_content()
    )

    attachments = list(
        message.iter_attachments()
    )

    assert len(attachments) == 1

    assert (
        attachments[0].get_filename()
        == "business_report.txt"
    )


def test_create_email_missing_attachment(
    tmp_path,
):
    """Test that a missing attachment raises an error."""

    missing_attachment = (
        tmp_path / "missing_report.txt"
    )

    with pytest.raises(FileNotFoundError):
        create_email(
            sender="automation@example.com",
            recipient="manager@example.com",
            subject="Test Report",
            body="Test body",
            attachment_path=missing_attachment,
        )


def test_save_email(tmp_path):
    """Test that an email is saved as an .eml file."""

    attachment = (
        tmp_path / "business_report.txt"
    )

    attachment.write_text(
        "Business Report",
        encoding="utf-8",
    )

    message = create_email(
        sender="automation@example.com",
        recipient="manager@example.com",
        subject="Business Performance Report",
        body="Attached is the business report.",
        attachment_path=attachment,
    )

    output_file = (
        tmp_path / "email_preview.eml"
    )

    save_email(
        message,
        output_file,
    )

    assert output_file.exists()

    email_contents = (
        output_file.read_bytes()
    )

    assert (
        b"Business Performance Report"
        in email_contents
    )
