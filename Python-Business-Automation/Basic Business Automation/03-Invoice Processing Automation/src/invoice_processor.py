from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = {
    "Invoice ID",
    "Customer",
    "Product",
    "Quantity",
    "Unit Price",
}


def load_invoice_data(file_path: Path) -> pd.DataFrame:
    """Load invoice data from a CSV file."""

    if not file_path.exists():
        raise FileNotFoundError(
            f"Invoice file not found: {file_path}"
        )

    return pd.read_csv(file_path)


def validate_required_columns(dataframe: pd.DataFrame) -> None:
    """Validate that all required columns exist."""

    missing_columns = REQUIRED_COLUMNS - set(dataframe.columns)

    if missing_columns:
        missing = ", ".join(sorted(missing_columns))

        raise ValueError(
            f"Missing required columns: {missing}"
        )


def identify_invalid_records(
    dataframe: pd.DataFrame,
) -> pd.Series:
    """Return a boolean mask identifying invalid invoice records."""

    invalid_records = (
        dataframe["Invoice ID"].isna()
        | dataframe["Customer"].isna()
        | dataframe["Product"].isna()
        | dataframe["Quantity"].isna()
        | dataframe["Unit Price"].isna()
        | (dataframe["Quantity"] <= 0)
        | (dataframe["Unit Price"] <= 0)
    )

    return invalid_records


def separate_valid_and_invalid_records(
    dataframe: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Separate valid and invalid invoice records."""

    invalid_mask = identify_invalid_records(dataframe)

    invalid_records = dataframe[
        invalid_mask
    ].copy()

    valid_records = dataframe[
        ~invalid_mask
    ].copy()

    return valid_records, invalid_records


def calculate_line_totals(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """Calculate the total for each invoice line item."""

    dataframe = dataframe.copy()

    dataframe["Line Total"] = (
        dataframe["Quantity"]
        * dataframe["Unit Price"]
    )

    return dataframe


def calculate_invoice_summary(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """Calculate the total value of each invoice."""

    invoice_summary = (
        dataframe.groupby("Invoice ID")
        .agg(
            Customer=("Customer", "first"),
            Invoice_Total=("Line Total", "sum"),
            Line_Items=("Invoice ID", "size"),
        )
        .reset_index()
        .sort_values("Invoice ID")
    )

    return invoice_summary


def calculate_processing_summary(
    valid_records: pd.DataFrame,
    invalid_records: pd.DataFrame,
    invoice_summary: pd.DataFrame,
) -> dict:
    """Calculate overall processing statistics."""

    total_records = (
        len(valid_records)
        + len(invalid_records)
    )

    total_invoice_value = (
        invoice_summary["Invoice_Total"].sum()
        if not invoice_summary.empty
        else 0
    )

    return {
        "Total Records Processed": total_records,
        "Valid Records": len(valid_records),
        "Invalid Records": len(invalid_records),
        "Invoices Processed": len(invoice_summary),
        "Total Invoice Value": total_invoice_value,
    }


def generate_output_files(
    valid_records: pd.DataFrame,
    invalid_records: pd.DataFrame,
    invoice_summary: pd.DataFrame,
    processing_summary: dict,
    output_directory: Path,
) -> None:
    """Generate processed invoice output files."""

    output_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    valid_records.to_csv(
        output_directory / "processed_invoices.csv",
        index=False,
    )

    invalid_records.to_csv(
        output_directory / "invalid_records.csv",
        index=False,
    )

    invoice_summary.to_csv(
        output_directory / "invoice_summary.csv",
        index=False,
    )

    summary_file = (
        output_directory
        / "processing_summary.txt"
    )

    with summary_file.open(
        "w",
        encoding="utf-8",
    ) as file:

        file.write("INVOICE PROCESSING SUMMARY\n")
        file.write("=" * 40 + "\n\n")

        for metric, value in processing_summary.items():

            if metric == "Total Invoice Value":
                file.write(
                    f"{metric}: ${value:,.2f}\n"
                )
            else:
                file.write(
                    f"{metric}: {value}\n"
                )


def main() -> None:
    """Run the Invoice Data Processing Automation."""

    project_directory = Path(
        __file__
    ).resolve().parent.parent

    input_file = (
        project_directory
        / "sample_data"
        / "invoices.csv"
    )

    output_directory = (
        project_directory
        / "output"
    )

    print("Invoice Data Processing Automation")
    print("-" * 45)

    try:
        # Load invoice data
        invoice_data = load_invoice_data(input_file)

        # Validate required columns
        validate_required_columns(invoice_data)

        # Separate valid and invalid records
        valid_records, invalid_records = (
            separate_valid_and_invalid_records(
                invoice_data
            )
        )

        # Calculate line totals
        valid_records = calculate_line_totals(
            valid_records
        )

        # Calculate invoice totals
        invoice_summary = (
            calculate_invoice_summary(
                valid_records
            )
        )

        # Calculate processing statistics
        processing_summary = (
            calculate_processing_summary(
                valid_records,
                invalid_records,
                invoice_summary,
            )
        )

        # Generate output files
        generate_output_files(
            valid_records,
            invalid_records,
            invoice_summary,
            processing_summary,
            output_directory,
        )

        print("\nProcessing completed successfully!\n")

        print("Processing Summary:")

        for metric, value in processing_summary.items():

            if metric == "Total Invoice Value":
                print(f"{metric}: ${value:,.2f}")
            else:
                print(f"{metric}: {value}")

        print(
            f"\nOutput files saved to: "
            f"{output_directory}"
        )

    except (
        FileNotFoundError,
        ValueError,
        KeyError,
    ) as error:

        print(f"\nError: {error}")


if __name__ == "__main__":
    main()
