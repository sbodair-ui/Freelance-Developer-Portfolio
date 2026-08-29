from pathlib import Path

import pandas as pd

REQUIRED_COLUMNS = {
"Date",
"Product",
"Category",
"Quantity",
"Unit Price",
}

def load_sales_data(file_path: Path) -> pd.DataFrame:
    """Load sales data from an Excel file."""

if not file_path.exists():
    raise FileNotFoundError(
        f"Sales data file not found: {file_path}"
    )

return pd.read_excel(file_path)

def validate_sales_data(dataframe: pd.DataFrame) -> None:
    """Validate that the required columns exist."""

missing_columns = REQUIRED_COLUMNS - set(dataframe.columns)

if missing_columns:
    missing = ", ".join(sorted(missing_columns))

    raise ValueError(
        f"Missing required columns: {missing}"
    )

def calculate_revenue(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Calculate revenue for each sales record."""

dataframe = dataframe.copy()

dataframe["Revenue"] = (
    dataframe["Quantity"]
    * dataframe["Unit Price"]
)

return dataframe

def calculate_business_metrics(
dataframe: pd.DataFrame,
) -> dict:
    """Calculate key business metrics."""

total_revenue = dataframe["Revenue"].sum()

total_orders = len(dataframe)

total_units_sold = dataframe["Quantity"].sum()

average_order_value = (
    total_revenue / total_orders
    if total_orders > 0
    else 0
)

return {
    "Total Revenue": total_revenue,
    "Total Orders": total_orders,
    "Total Units Sold": total_units_sold,
    "Average Order Value": average_order_value,
}

def analyze_product_performance(
dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """Analyze sales performance by product."""

product_performance = (
    dataframe.groupby("Product")
    .agg(
        Total_Units_Sold=(
            "Quantity",
            "sum",
        ),
        Total_Revenue=(
            "Revenue",
            "sum",
        ),
    )
    .reset_index()
    .sort_values(
        by="Total_Revenue",
        ascending=False,
    )
)

return product_performance

def analyze_category_performance(
dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """Analyze sales performance by category."""

category_performance = (
    dataframe.groupby("Category")
    .agg(
        Total_Units_Sold=(
            "Quantity",
            "sum",
        ),
        Total_Revenue=(
            "Revenue",
            "sum",
        ),
    )
    .reset_index()
    .sort_values(
        by="Total_Revenue",
        ascending=False,
    )
)

return category_performance

def generate_excel_report(
metrics: dict,
product_performance: pd.DataFrame,
category_performance: pd.DataFrame,
output_file: Path,
) -> None:
    """Generate a multi-sheet Excel business report."""

summary_dataframe = pd.DataFrame(
    list(metrics.items()),
    columns=["Metric", "Value"],
)

with pd.ExcelWriter(
    output_file,
    engine="openpyxl",
) as writer:

    summary_dataframe.to_excel(
        writer,
        sheet_name="Summary",
        index=False,
    )

    product_performance.to_excel(
        writer,
        sheet_name="Product Performance",
        index=False,
    )

    category_performance.to_excel(
        writer,
        sheet_name="Category Performance",
        index=False,
    )

def main() -> None:
    """Run the Excel Report Generator."""

project_directory = Path(__file__).resolve().parent.parent

input_file = (
    project_directory
    / "sample_data"
    / "sales_data.xlsx"
)

output_directory = project_directory / "output"

output_directory.mkdir(exist_ok=True)

output_file = (
    output_directory
    / "business_report.xlsx"
)

print("Excel Report Generator")
print("-" * 40)

try:
    # Load and validate data
    sales_data = load_sales_data(input_file)

    validate_sales_data(sales_data)

    # Calculate revenue
    sales_data = calculate_revenue(sales_data)

    # Calculate business metrics
    metrics = calculate_business_metrics(sales_data)

    # Analyze performance
    product_performance = (
        analyze_product_performance(sales_data)
    )

    category_performance = (
        analyze_category_performance(sales_data)
    )

    # Generate report
    generate_excel_report(
        metrics,
        product_performance,
        category_performance,
        output_file,
    )

    print("\nReport generated successfully!")

    print(f"\nOutput file: {output_file}")

    print("\nBusiness Metrics:")

    for metric, value in metrics.items():

        if "Revenue" in metric or "Value" in metric:
            print(f"{metric}: ${value:,.2f}")

        else:
            print(f"{metric}: {value}")

except (
    FileNotFoundError,
    ValueError,
    KeyError,
) as error:

    print(f"\nError: {error}")

if **name** == "**main**":
main()

