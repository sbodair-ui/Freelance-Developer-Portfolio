import pandas as pd


def calculate_total_revenue(data):
    """Calculate total revenue."""
    return data["Revenue"].sum()


def calculate_total_expenses(data):
    """Calculate total expenses."""
    return data["Expenses"].sum()


def calculate_net_revenue(data):
    """Calculate net revenue."""
    return calculate_total_revenue(data) - calculate_total_expenses(data)


def calculate_profit_margin(data):
    """Calculate profit margin as a percentage."""
    total_revenue = calculate_total_revenue(data)

    if total_revenue == 0:
        return 0.0

    net_revenue = calculate_net_revenue(data)

    return (net_revenue / total_revenue) * 100


def calculate_total_units(data):
    """Calculate total units."""
    return data["Units"].sum()


def calculate_total_transactions(data):
    """Calculate total transactions."""
    return data["Transactions"].sum()


def calculate_average_transaction_value(data):
    """Calculate average transaction value."""
    total_transactions = calculate_total_transactions(data)

    if total_transactions == 0:
        return 0.0

    return calculate_total_revenue(data) / total_transactions


def calculate_all_kpis(data):
    """
    Calculate all primary business KPIs.

    Args:
        data: Validated business data as a pandas DataFrame.

    Returns:
        dict: Dictionary containing calculated KPIs.
    """
    return {
        "total_revenue": calculate_total_revenue(data),
        "total_expenses": calculate_total_expenses(data),
        "net_revenue": calculate_net_revenue(data),
        "profit_margin": calculate_profit_margin(data),
        "total_units": calculate_total_units(data),
        "total_transactions": calculate_total_transactions(data),
        "average_transaction_value": calculate_average_transaction_value(data),
    }
