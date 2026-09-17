from pathlib import Path
import sys

import pandas as pd
import pytest


# Add the src folder to Python's import path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_DIRECTORY = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_DIRECTORY))


from report_generator import (
    load_sales_data,
    validate_sales_data,
    calculate_revenue,
    calculate_business_metrics,
    analyze_product_performance,
    analyze_category_performance,
    generate_excel_report,
)


def create_test_dataframe():
    """Create sample sales data for testing."""

    return pd.DataFrame(
        {
            "Date": [
                "2026-01-05",
                "2026-01-06",
                "2026-01-07",
            ],
            "Product": [
                "Laptop",
                "Mouse",
                "Laptop",
            ],
            "Category": [
                "Electronics",
                "Electronics",
                "Electronics",
            ],
            "Units Sold": [
                2,
                5,
                1,
            ],
            "Unit Price": [
                1000.00,
                25.00,
                1000.00,
            ],
        }
    )


def test_validate_sales_data():
    """Test that valid sales data passes validation."""

    dataframe = create_test_dataframe()

    validate_sales_data(dataframe)


def test_validate_sales_data_missing_column():
    """Test that missing required columns raise ValueError."""

    dataframe = pd.DataFrame(
        {
            "Product": ["Laptop"],
            "Units Sold": [2],
        }
    )

    with pytest.raises(ValueError):
        validate_sales_data(dataframe)


def test_calculate_revenue():
    """Test revenue calculation."""

    dataframe = create_test_dataframe()

    result = calculate_revenue(dataframe)

    expected_revenue = [
        2000.00,
        125.00,
        1000.00,
    ]

    assert result["Revenue"].tolist() == expected_revenue


def test_calculate_business_metrics():
    """Test business metric calculations."""

    dataframe = create_test_dataframe()

    dataframe = calculate_revenue(dataframe)

    metrics = calculate_business_metrics(dataframe)

    assert metrics["Total Revenue"] == 3125.00
    assert metrics["Total Orders"] == 3
    assert metrics["Total Units Sold"] == 8
    assert metrics["Average Order Value"] == pytest.approx(
        1041.67,
        abs=0.01,
    )


def test_analyze_product_performance():
    """Test product performance analysis."""

    dataframe = create_test_dataframe()

    dataframe = calculate_revenue(dataframe)

    result = analyze_product_performance(dataframe)

    laptop_data = result[
        result["Product"] == "Laptop"
    ].iloc[0]

    assert laptop_data["Total_Units_Sold"] == 3
    assert laptop_data["Total_Revenue"] == 3000.00


def test_analyze_category_performance():
    """Test category performance analysis."""

    dataframe = create_test_dataframe()

    dataframe = calculate_revenue(dataframe)

    result = analyze_category_performance(dataframe)

    electronics_data = result[
        result["Category"] == "Electronics"
    ].iloc[0]

    assert electronics_data["Total_Units_Sold"] == 8
    assert electronics_data["Total_Revenue"] == 3125.00


def test_generate_excel_report(tmp_path):
    """Test that an Excel report is generated."""

    dataframe = create_test_dataframe()

    dataframe = calculate_revenue(dataframe)

    metrics = calculate_business_metrics(dataframe)

    product_performance = analyze_product_performance(
        dataframe
    )

    category_performance = analyze_category_performance(
        dataframe
    )

    output_file = tmp_path / "test_report.xlsx"

    generate_excel_report(
        metrics,
        product_performance,
        category_performance,
        output_file,
    )

    assert output_file.exists()

    excel_file = pd.ExcelFile(output_file)

    assert "Summary" in excel_file.sheet_names
    assert "Product Performance" in excel_file.sheet_names
    assert "Category Performance" in excel_file.sheet_names
