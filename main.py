from utils.file_handler import read_sales_data
from utils.data_processor import (
    parse_transactions,
    validate_and_filter,
    calculate_total_revenue
)
from utils.api_handler import (
    fetch_all_products,
    create_product_mapping,
    enrich_sales_data,
    save_enriched_data
)
from utils.report_generator import generate_sales_report


DATA_FILE = "data/sales_data.txt"


def main():
    try:
        # Step 1: Read raw data
        print("Reading sales data...")
        raw_lines = read_sales_data(DATA_FILE)
        print(f"Total records read: {len(raw_lines)}")

        # Step 2: Parse transactions
        print("Parsing transactions...")
        parsed_transactions = parse_transactions(raw_lines)
        print(f"Parsed records: {len(parsed_transactions)}")

        # Step 3: Validate and filter
        print("Validating transactions...")
        valid_transactions, invalid_count, summary = validate_and_filter(parsed_transactions)
        print(f"Invalid records removed: {invalid_count}")
        print(f"Valid records after cleaning: {len(valid_transactions)}")

        # Step 4: Basic analysis
        total_revenue = calculate_total_revenue(valid_transactions)
        print(f"Total Revenue: ₹{round(total_revenue, 2)}")

        # Step 5: Fetch product data from API
        print("Fetching product data from API...")
        api_products = fetch_all_products()

        # Step 6: Create product mapping
        product_mapping = create_product_mapping(api_products)

        # Step 7: Enrich sales data
        print("Enriching sales data...")
        enriched_transactions, enrich_stats = enrich_sales_data(
            valid_transactions,
            product_mapping
        )
        print(
            f"Enriched {enrich_stats['enriched']} out of "
            f"{enrich_stats['total']} transactions"
        )

        # Step 8: Save enriched data
        enriched_file = save_enriched_data(enriched_transactions)
        print(f"Enriched data saved to: {enriched_file}")

        # Step 9: Generate report
        report_file = generate_sales_report(
            valid_transactions,
            enriched_transactions
        )
        print(f"Sales report generated at: {report_file}")

        print("Processing complete.")

    except Exception as e:
        print("An error occurred:", e)


if __name__ == "__main__":
    main()
