from pathlib import Path
from email.message import EmailMessage
import mimetypes
import pandas as pd


REQUIRED_COLUMNS = {
    "Date",
    "Department",
    "Revenue",
    "Expenses",
}


def load_business_data(file_path: Path) -> pd.DataFrame:
    """Load business data from a CSV file."""

    if not file_path.exists():
        raise FileNotFoundError(
            f"Business data file not found: {file_path}"
        )

    return pd.read_csv(file_path)


def validate_business_data(
    dataframe: pd.DataFrame,
) -> None:
    """Validate required business data columns."""

    missing_columns = (
        REQUIRED_COLUMNS - set(dataframe.columns)
    )

    if missing_columns:
        missing = ", ".join(sorted(missing_columns))

        raise ValueError(
            f"Missing required columns: {missing}"
        )


def calculate_business_metrics(
    dataframe: pd.DataFrame,
) -> dict:
    """Calculate business performance metrics."""

    total_revenue = dataframe["Revenue"].sum()

    total_expenses = dataframe["Expenses"].sum()

    net_revenue = total_revenue - total_expenses

    average_revenue = (
        total_revenue / len(dataframe)
        if len(dataframe) > 0
        else 0
    )

    return {
        "Total Revenue": total_revenue,
        "Total Expenses": total_expenses,
        "Net Revenue": net_revenue,
        "Average Revenue": average_revenue,
    }


def analyze_department_performance(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """Calculate revenue and expenses by department."""

    department_performance = (
        dataframe.groupby("Department")
        .agg(
            Total_Revenue=("Revenue", "sum"),
            Total_Expenses=("Expenses", "sum"),
        )
        .reset_index()
    )

    department_performance["Net_Revenue"] = (
        department_performance["Total_Revenue"]
        - department_performance["Total_Expenses"]
    )

    return department_performance.sort_values(
        by="Total_Revenue",
        ascending=False,
    )


def generate_report(
    dataframe: pd.DataFrame,
    metrics: dict,
    department_performance: pd.DataFrame,
    output_file: Path,
) -> None:
    """Generate a business report."""

    report_lines = [
        "BUSINESS PERFORMANCE REPORT",
        "=" * 40,
        "",
        "Overall Metrics",
        "-" * 40,
    ]

    for metric, value in metrics.items():
        report_lines.append(
            f"{metric}: ${value:,.2f}"
        )

    report_lines.extend(
        [
            "",
            "Department Performance",
            "-" * 40,
        ]
    )

    for _, row in department_performance.iterrows():
        report_lines.append(
            f"{row['Department']}: "
            f"Revenue ${row['Total_Revenue']:,.2f}, "
            f"Expenses ${row['Total_Expenses']:,.2f}, "
            f"Net ${row['Net_Revenue']:,.2f}"
        )

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_file.write_text(
        "\n".join(report_lines),
        encoding="utf-8",
    )


def create_email(
    sender: str,
    recipient: str,
    subject: str,
    body: str,
    attachment_path: Path,
) -> EmailMessage:
    """Create an email with a report attachment."""

    if not attachment_path.exists():
        raise FileNotFoundError(
            f"Attachment not found: {attachment_path}"
        )

    message = EmailMessage()

    message["From"] = sender
    message["To"] = recipient
    message["Subject"] = subject

    message.set_content(body)

    mime_type, _ = mimetypes.guess_type(
        attachment_path.name
    )

    if mime_type is None:
        mime_type = "application/octet-stream"

    maintype, subtype = mime_type.split(
        "/",
        1,
    )

    with attachment_path.open("rb") as file:
        message.add_attachment(
            file.read(),
            maintype=maintype,
            subtype=subtype,
            filename=attachment_path.name,
        )

    return message


def save_email(
    message: EmailMessage,
    output_file: Path,
) -> None:
    """Save the email locally as an .eml file."""

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_file.write_bytes(
        message.as_bytes()
    )


def main() -> None:
    """Run the Email Report Automation."""

    project_directory = (
        Path(__file__).resolve().parent.parent
    )

    input_file = (
        project_directory
        / "sample_data"
        / "business_data.csv"
    )

    output_directory = (
        project_directory
        / "output"
    )

    report_file = (
        output_directory
        / "business_report.txt"
    )

    email_file = (
        output_directory
        / "email_preview.eml"
    )

    print("Email Report Automation")
    print("-" * 40)

    try:
        # Load data
        business_data = load_business_data(
            input_file
        )

        # Validate data
        validate_business_data(
            business_data
        )

        # Calculate metrics
        metrics = calculate_business_metrics(
            business_data
        )

        # Analyze departments
        department_performance = (
            analyze_department_performance(
                business_data
            )
        )

        # Generate report
        generate_report(
            business_data,
            metrics,
            department_performance,
            report_file,
        )

        # Create email
        email_body = (
            "Hello,\n\n"
            "Attached is the latest business "
            "performance report.\n\n"
            f"Total Revenue: "
            f"${metrics['Total Revenue']:,.2f}\n"
            f"Total Expenses: "
            f"${metrics['Total Expenses']:,.2f}\n"
            f"Net Revenue: "
            f"${metrics['Net Revenue']:,.2f}\n\n"
            "Regards,\n"
            "Automated Reporting System"
        )

        message = create_email(
            sender="automation@example.com",
            recipient="manager@example.com",
            subject="Business Performance Report",
            body=email_body,
            attachment_path=report_file,
        )

        # Save email locally
        save_email(
            message,
            email_file,
        )

        print("\nReport generated successfully!")
        print(f"Report: {report_file}")

        print("\nEmail preview generated!")
        print(f"Email: {email_file}")

        print("\nBusiness Metrics:")

        for metric, value in metrics.items():
            print(
                f"{metric}: ${value:,.2f}"
            )

    except (
        FileNotFoundError,
        ValueError,
        KeyError,
    ) as error:

        print(f"\nError: {error}")


if __name__ == "__main__":
    main()
