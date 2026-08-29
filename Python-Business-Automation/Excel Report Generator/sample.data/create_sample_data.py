from pathlib import Path

import pandas as pd

def create_sample_data():
"""Create sample sales data for the Excel Report Generator."""

```
data = {
    "Date": [
        "2026-01-05",
        "2026-01-06",
        "2026-01-07",
        "2026-01-08",
        "2026-01-09",
        "2026-01-10",
        "2026-01-11",
        "2026-01-12",
        "2026-01-13",
        "2026-01-14",
    ],
    "Product": [
        "Laptop",
        "Mouse",
        "Desk",
        "Keyboard",
        "Monitor",
        "Office Chair",
        "Laptop",
        "Mouse",
        "Desk",
        "Monitor",
    ],
    "Category": [
        "Electronics",
        "Electronics",
        "Furniture",
        "Electronics",
        "Electronics",
        "Furniture",
        "Electronics",
        "Electronics",
        "Furniture",
        "Electronics",
    ],
    "Quantity": [
        2,
        5,
        1,
        3,
        2,
        1,
        1,
        10,
        2,
        3,
    ],
    "Unit Price": [
        899.99,
        25.00,
        350.00,
        75.00,
        250.00,
        175.00,
        899.99,
        25.00,
        350.00,
        250.00,
    ],
}

dataframe = pd.DataFrame(data)

output_file = Path(__file__).parent / "sales_data.xlsx"

dataframe.to_excel(
    output_file,
    index=False,
)

print(f"Sample data created: {output_file}")
```

if **name** == "**main**":
create_sample_data()


