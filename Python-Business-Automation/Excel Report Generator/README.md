# 📊 Excel Report Generator

A Python business automation tool that transforms raw sales data into a structured and professional Excel report.

## 🚀 Project Overview

Businesses often store sales information in spreadsheets, but manually analyzing that data and creating reports can be time-consuming.

The **Excel Report Generator** automates this process by:

* Reading raw sales data from an Excel file
* Validating and processing the data
* Calculating important business metrics
* Analyzing product performance
* Analyzing category performance
* Generating a professional Excel report automatically

This project demonstrates how Python can automate repetitive business reporting tasks and turn raw data into useful business insights.

---

## ✨ Features

* 📥 Read sales data from Excel files
* ✅ Validate required data columns
* 📊 Calculate key business metrics
* 💰 Calculate total revenue
* 🛒 Calculate total orders
* 📦 Calculate total units sold
* 📈 Calculate average order value
* 🏆 Analyze product performance
* 📂 Analyze category performance
* 📄 Generate a multi-sheet Excel report
* 🎨 Apply professional formatting to generated reports
* 🧪 Include automated unit tests

---

## 🔄 How It Works

```text
Raw Sales Data
       ↓
Read Excel File
       ↓
Validate Data
       ↓
Process Sales Information
       ↓
Calculate Business Metrics
       ↓
Analyze Products & Categories
       ↓
Generate Excel Report
```

---

## 📁 Project Structure

```text
Excel-Report-Generator/
│
├── README.md
├── requirements.txt
│
├── src/
│   └── report_generator.py
│
├── tests/
│   └── test_report_generator.py
│
└── sample_data/
    └── sales_data.xlsx
```

---

## 📊 Input Data

The application processes sales data containing information such as:

| Date       | Product | Category    | Quantity | Unit Price |
| ---------- | ------- | ----------- | -------- | ---------: |
| 2026-01-05 | Laptop  | Electronics | 2        |     899.99 |
| 2026-01-06 | Mouse   | Electronics | 5        |      25.00 |
| 2026-01-07 | Desk    | Furniture   | 1        |     350.00 |

The application will calculate revenue using:

```text
Revenue = Quantity × Unit Price
```

---

## 📈 Generated Report

The generated Excel report will contain multiple worksheets.

### 📋 Summary

Provides an overview of important business metrics:

* Total Revenue
* Total Orders
* Total Units Sold
* Average Order Value

### 🏆 Product Performance

Shows sales and revenue information for each product.

### 📂 Category Performance

Shows revenue performance grouped by product category.

---

## 🛠️ Technologies Used

* **Python**
* **pandas** — Data processing and analysis
* **openpyxl** — Excel file generation and formatting
* **pytest** — Automated testing

---

## ⚙️ Installation

Clone the repository:

```bash
git clone <repository-url>
```

Navigate to the project directory:

```bash
cd Excel-Report-Generator
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Usage

Run the application from the project directory:

```bash
python src/report_generator.py
```

The program will:

1. Load the sales data
2. Validate the information
3. Calculate business metrics
4. Generate performance summaries
5. Create an Excel report

---

## 🧪 Running Tests

Run the automated tests using:

```bash
pytest
```

The tests verify important functionality such as:

* Data validation
* Revenue calculations
* Business metric calculations
* Product performance analysis
* Category performance analysis
* Report generation

---

## 🎯 Skills Demonstrated

This project demonstrates practical skills in:

* Python programming
* Business automation
* Data processing
* Data validation
* Excel automation
* Data analysis
* Report generation
* File handling
* Automated testing
* Software project organization

---

## 🔮 Future Improvements

Potential future enhancements include:

* 📊 Automatic charts and graphs
* 📅 Date range filtering
* 📈 Monthly and quarterly reports
* 🏆 Top-performing product analysis
* 📉 Sales trend analysis
* 🎨 Additional report formatting options
* 💻 Command-line arguments
* ⚙️ Configuration files
* 📧 Automatic email delivery of reports

---

## 👨‍💻 Author

**Stephen Bodair**

Freelance Developer | Python Automation | Business Solutions

---

## 📄 License

This project is available for educational and portfolio purposes.

