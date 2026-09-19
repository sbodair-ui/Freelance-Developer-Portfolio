from src.kpi_data_loader import load_business_data
from src.trend_analyzer import (
    analyze_monthly_performance,
    analyze_department_performance,
    analyze_product_performance,
    analyze_all_trends,
)


DATA_FILE = "sample_data/business_data.csv"


def test_monthly_performance():
    data = load_business_data(DATA_FILE)

    result = analyze_monthly_performance(data)

    assert len(result) == 9
    assert "Month" in result.columns
    assert "Revenue" in result.columns
    assert "Expenses" in result.columns
    assert "Net Revenue" in result.columns
    assert "Profit Margin" in result.columns


def test_department_performance():
    data = load_business_data(DATA_FILE)

    result = analyze_department_performance(data)

    assert len(result) == 4
    assert "Department" in result.columns
    assert "Revenue" in result.columns
    assert "Net Revenue" in result.columns


def test_product_performance():
    data = load_business_data(DATA_FILE)

    result = analyze_product_performance(data)

    assert len(result) == 5
    assert "Product" in result.columns
    assert "Revenue" in result.columns
    assert "Net Revenue" in result.columns


def test_all_trends():
    data = load_business_data(DATA_FILE)

    results = analyze_all_trends(data)

    assert "monthly_performance" in results
    assert "department_performance" in results
    assert "product_performance" in results
