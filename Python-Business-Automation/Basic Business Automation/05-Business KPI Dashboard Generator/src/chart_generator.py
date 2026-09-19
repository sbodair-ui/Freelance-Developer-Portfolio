from pathlib import Path

import matplotlib.pyplot as plt


def create_output_directory(output_directory):
    """Create the output directory if it does not exist."""
    output_directory = Path(output_directory)
    output_directory.mkdir(parents=True, exist_ok=True)
    return output_directory


def create_monthly_revenue_chart(monthly_data, output_directory):
    """Create a line chart showing monthly revenue."""
    output_directory = create_output_directory(output_directory)

    plt.figure(figsize=(10, 6))

    plt.plot(
        monthly_data["Month"],
        monthly_data["Revenue"],
        marker="o",
    )

    plt.title("Monthly Revenue Trend")
    plt.xlabel("Month")
    plt.ylabel("Revenue")
    plt.xticks(rotation=45)
    plt.tight_layout()

    output_path = output_directory / "monthly_revenue_trend.png"
    plt.savefig(output_path)
    plt.close()

    return output_path


def create_department_performance_chart(
    department_data,
    output_directory,
):
    """Create a bar chart showing revenue by department."""
    output_directory = create_output_directory(output_directory)

    plt.figure(figsize=(10, 6))

    plt.bar(
        department_data["Department"],
        department_data["Revenue"],
    )

    plt.title("Revenue by Department")
    plt.xlabel("Department")
    plt.ylabel("Revenue")
    plt.xticks(rotation=45)
    plt.tight_layout()

    output_path = output_directory / "department_performance.png"
    plt.savefig(output_path)
    plt.close()

    return output_path


def create_product_performance_chart(
    product_data,
    output_directory,
):
    """Create a bar chart showing revenue by product."""
    output_directory = create_output_directory(output_directory)

    plt.figure(figsize=(10, 6))

    plt.bar(
        product_data["Product"],
        product_data["Revenue"],
    )

    plt.title("Revenue by Product")
    plt.xlabel("Product")
    plt.ylabel("Revenue")
    plt.xticks(rotation=45)
    plt.tight_layout()

    output_path = output_directory / "product_performance.png"
    plt.savefig(output_path)
    plt.close()

    return output_path


def create_all_charts(
    monthly_data,
    department_data,
    product_data,
    output_directory,
):
    """
    Create all dashboard charts.

    Returns:
        dict: Paths to generated chart files.
    """
    return {
        "monthly_revenue": create_monthly_revenue_chart(
            monthly_data,
            output_directory,
        ),
        "department_performance": create_department_performance_chart(
            department_data,
            output_directory,
        ),
        "product_performance": create_product_performance_chart(
            product_data,
            output_directory,
        ),
    }
