from utils.file_handler import read_sales_data
from utils.data_processor import clean_sales_data
from utils.api_handler import get_product_info
import os

DATA_PATH = "data/sales_data.txt"
OUTPUT_PATH = "output/summary_report.txt"


def generate_report(cleaned_data, total_parsed, invalid_removed):
    # Calculate total revenue
    total_revenue = sum(
        record["Quantity"] * record["UnitPrice"]
        for record in cleaned_data
    )

    # Ensure output directory exists
    os.makedirs("output", exist_ok=True)

    # Write summary report to file
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(f"Total records parsed: {total_parsed}\n")
        f.write(f"Invalid records removed: {invalid_removed}\n")
        f.write(f"Valid records after cleaning: {len(cleaned_data)}\n")
        f.write(f"Total Revenue: ₹{round(total_revenue, 2)}\n")

    # Print results to console (as required)
    print(f"Total Revenue: ₹{round(total_revenue, 2)}")

    # Demonstrate API usage (explicit requirement)
    sample_product = get_product_info("P107")
    print("Sample product info from API:", sample_product)


def main():
    # Step 1: Read raw sales data
    raw_records = read_sales_data(DATA_PATH)
    total_parsed = len(raw_records)

    # Step 2: Clean and validate data
    cleaned_records = clean_sales_data(raw_records)
    invalid_removed = total_parsed - len(cleaned_records)

    # Step 3: Generate report
    generate_report(cleaned_records, total_parsed, invalid_removed)


if __name__ == "__main__":
    main()
