import pandas as pd


def analyze_monthly_performance(data):
    """
    Calculate monthly business performance.

    Args:
        data: Validated business data as a pandas DataFrame.

    Returns:
        pandas.DataFrame: Monthly performance summary.
    """
    monthly_data = data.copy()

    monthly_data["Month"] = monthly_data["Date"].dt.to_period("M")

    monthly_performance = (
        monthly_data.groupby("Month")
        .agg(
            Revenue=("Revenue", "sum"),
            Expenses=("Expenses", "sum"),
            Units=("Units", "sum"),
            Transactions=("Transactions", "sum"),
        )
        .reset_index()
    )

    monthly_performance["Net Revenue"] = (
        monthly_performance["Revenue"]
        - monthly_performance["Expenses"]
    )

    monthly_performance["Profit Margin"] = (
        monthly_performance["Net Revenue"]
        / monthly_performance["Revenue"]
        * 100
    )

    monthly_performance["Month"] = (
        monthly_performance["Month"]
        .astype(str)
    )

    return monthly_performance


def analyze_department_performance(data):
    """
    Calculate business performance by department.

    Args:
        data: Validated business data as a pandas DataFrame.

    Returns:
        pandas.DataFrame: Department performance summary.
    """
    department_performance = (
        data.groupby("Department")
        .agg(
            Revenue=("Revenue", "sum"),
            Expenses=("Expenses", "sum"),
            Units=("Units", "sum"),
            Transactions=("Transactions", "sum"),
        )
        .reset_index()
    )

    department_performance["Net Revenue"] = (
        department_performance["Revenue"]
        - department_performance["Expenses"]
    )

    department_performance["Profit Margin"] = (
        department_performance["Net Revenue"]
        / department_performance["Revenue"]
        * 100
    )

    return department_performance


def analyze_product_performance(data):
    """
    Calculate business performance by product.

    Args:
        data: Validated business data as a pandas DataFrame.

    Returns:
        pandas.DataFrame: Product performance summary.
    """
    product_performance = (
        data.groupby("Product")
        .agg(
            Revenue=("Revenue", "sum"),
            Expenses=("Expenses", "sum"),
            Units=("Units", "sum"),
            Transactions=("Transactions", "sum"),
        )
        .reset_index()
    )

    product_performance["Net Revenue"] = (
        product_performance["Revenue"]
        - product_performance["Expenses"]
    )

    product_performance["Profit Margin"] = (
        product_performance["Net Revenue"]
        / product_performance["Revenue"]
        * 100
    )

    return product_performance


def analyze_all_trends(data):
    """
    Run all trend and performance analyses.

    Args:
        data: Validated business data as a pandas DataFrame.

    Returns:
        dict: Collection of analysis DataFrames.
    """
    return {
        "monthly_performance": analyze_monthly_performance(data),
        "department_performance": analyze_department_performance(data),
        "product_performance": analyze_product_performance(data),
    }
