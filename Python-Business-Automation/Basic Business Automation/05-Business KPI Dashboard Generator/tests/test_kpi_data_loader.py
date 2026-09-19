import pandas as pd
import pytest

from src.kpi_data_loader import (
    load_business_data,
    validate_columns,
    validate_numeric_columns,
    validate_business_data,
)


def test_load_business_data():
    data = load_business_data("sample_data/business_data.csv")

    assert isinstance(data, pd.DataFrame)
    assert len(data) == 45
    assert len(data.columns) == 7


def test_required_columns():
    data = load_business_data("sample_data/business_data.csv")

    required_columns = [
        "Date",
        "Department",
        "Product",
        "Revenue",
        "Expenses",
        "Units",
        "Transactions",
    ]

    for column in required_columns:
        assert column in data.columns


def test_missing_file():
    with pytest.raises(FileNotFoundError):
        load_business_data("sample_data/missing.csv")


def test_missing_columns():
    data = pd.DataFrame(
        {
            "Date": ["2026-01-01"],
            "Revenue": [1000],
        }
    )

    with pytest.raises(ValueError):
        validate_columns(data)


def test_numeric_columns():
    data = load_business_data("sample_data/business_data.csv")

    validate_numeric_columns(data)


def test_empty_data():
    data = pd.DataFrame(
        columns=[
            "Date",
            "Department",
            "Product",
            "Revenue",
            "Expenses",
            "Units",
            "Transactions",
        ]
    )

    with pytest.raises(ValueError):
        validate_business_data(data)


def test_negative_revenue():
    data = pd.DataFrame(
        {
            "Date": ["2026-01-01"],
            "Department": ["Sales"],
            "Product": ["Software"],
            "Revenue": [-100],
            "Expenses": [50],
            "Units": [1],
            "Transactions": [1],
        }
    )

    with pytest.raises(ValueError):
        validate_business_data(data)
