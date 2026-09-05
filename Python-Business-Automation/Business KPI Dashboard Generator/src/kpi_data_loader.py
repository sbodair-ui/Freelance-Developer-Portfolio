from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = [
    "Date",
    "Department",
    "Product",
    "Revenue",
    "Expenses",
    "Units",
    "Transactions",
]


def load_business_data(file_path):
    """
    Load business data from a CSV file.

    Args:
        file_path: Path to the CSV file.

    Returns:
        pandas.DataFrame: Loaded business data.

    Raises:
        FileNotFoundError: If the CSV file does not exist.
        ValueError: If required columns are missing.
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"Data file not found: {file_path}")

    data = pd.read_csv(file_path)

    validate_columns(data)

    data["Date"] = pd.to_datetime(data["Date"])

    return data


def validate_columns(data):
    """
    Validate that all required columns exist.

    Args:
        data: pandas.DataFrame to validate.

    Raises:
        ValueError: If required columns are missing.
    """
    missing_columns = [
        column for column in REQUIRED_COLUMNS
        if column not in data.columns
    ]

    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing required columns: {missing}")


def validate_numeric_columns(data):
    """
    Validate that financial and quantity columns contain numeric values.

    Args:
        data: pandas.DataFrame to validate.

    Raises:
        ValueError: If numeric columns contain invalid values.
    """
    numeric_columns = [
        "Revenue",
        "Expenses",
        "Units",
        "Transactions",
    ]

    for column in numeric_columns:
        if not pd.api.types.is_numeric_dtype(data[column]):
            raise ValueError(
                f"Column '{column}' must contain numeric values."
            )


def validate_business_data(data):
    """
    Run all business data validation checks.

    Args:
        data: pandas.DataFrame to validate.

    Returns:
        bool: True when validation succeeds.
    """
    validate_columns(data)
    validate_numeric_columns(data)

    if data.empty:
        raise ValueError("Business data cannot be empty.")

    if data["Revenue"].lt(0).any():
        raise ValueError("Revenue cannot contain negative values.")

    if data["Expenses"].lt(0).any():
        raise ValueError("Expenses cannot contain negative values.")

    if data["Units"].lt(0).any():
        raise ValueError("Units cannot contain negative values.")

    if data["Transactions"].lt(0).any():
        raise ValueError("Transactions cannot contain negative values.")

    return True
