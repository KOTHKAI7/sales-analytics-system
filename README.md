# Sales Analytics System

## Overview
A Python-based system that reads, cleans, validates, analyzes, and reports on sales transaction data.  
The project also integrates with an external API to enrich transaction records and generates a comprehensive text report.

---

## Features
- Handles messy pipe-delimited sales data
- Cleans numeric and text formatting issues
- Removes invalid transactions based on validation rules
- Performs sales analytics and aggregations
- Integrates with DummyJSON API for product enrichment
- Generates detailed output reports

---

## Project Structure
sales-analytics-system/
├── README.md
├── main.py
├── requirements.txt
├── utils/
│ ├── file_handler.py
│ ├── data_processor.py
│ ├── api_handler.py
│ └── report_generator.py
├── data/
│ ├── sales_data.txt
│ └── enriched_sales_data.txt
└── output/
└── sales_report.txt

yaml
Copy code

---

## Requirements
- Python 3.x
- Install dependencies:
```bash
pip install -r requirements.txt
How to Run
Ensure sales_data.txt is present in the data/ folder

Run the program:

bash
Copy code
python main.py
Output
After execution, the system generates:

data/enriched_sales_data.txt — sales data enriched using API product information

output/sales_report.txt — a comprehensive sales analytics report

API Used
DummyJSON Products API

Used to fetch product metadata and enrich sales transactions
