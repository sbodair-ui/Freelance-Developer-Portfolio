import pandas as pd

from src.kpi_calculator import (
    calculate_total_revenue,
    calculate_total_expenses,
    calculate_net_revenue,
    calculate_profit_margin,
    calculate_total_units,
    calculate_total_transactions,
    calculate_average_transaction_value,
    calculate_all_kpis,
)


def create_test_data():
    return pd.DataFrame(
        {
            "Revenue": [1000, 2000],
            "Expenses": [400, 600],
            "Units": [10, 20],
            "Transactions": [5, 10],
        }
    )


def test_total_revenue():
    data = create_test_data()

    assert calculate_total_revenue(data) == 3000


def test_total_expenses():
    data = create_test_data()

    assert calculate_total_expenses(data) == 1000


def test_net_revenue():
    data = create_test_data()

    assert calculate_net_revenue(data) == 2000


def test_profit_margin():
    data = create_test_data()

    assert calculate_profit_margin(data) == 2000 / 3000 * 100


def test_total_units():
    data = create_test_data()

    assert calculate_total_units(data) == 30


def test_total_transactions():
    data = create_test_data()

    assert calculate_total_transactions(data) == 15


def test_average_transaction_value():
    data = create_test_data()

    assert calculate_average_transaction_value(data) == 200


def test_all_kpis():
    data = create_test_data()

    kpis = calculate_all_kpis(data)

    assert kpis["total_revenue"] == 3000
    assert kpis["total_expenses"] == 1000
    assert kpis["net_revenue"] == 2000
    assert kpis["total_units"] == 30
    assert kpis["total_transactions"] == 15
