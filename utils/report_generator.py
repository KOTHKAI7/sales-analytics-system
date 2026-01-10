from utils.data_processor import (
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day
)
from datetime import datetime
import os


def generate_sales_report(transactions, enriched_transactions, output_file="output/sales_report.txt"):
    """
    Generates a text-based sales analytics report.
    """

    os.makedirs("output", exist_ok=True)

    total_revenue = calculate_total_revenue(transactions)
    total_transactions = len(transactions)
    avg_order_value = total_revenue / total_transactions if total_transactions else 0

    dates = sorted({t["Date"] for t in transactions})
    date_range = f"{dates[0]} to {dates[-1]}" if dates else "N/A"

    region_stats = region_wise_sales(transactions)
    top_products = top_selling_products(transactions, n=5)
    customers = customer_analysis(transactions)
    daily_trend = daily_sales_trend(transactions)
    peak_day = find_peak_sales_day(transactions)

    enriched_count = sum(1 for t in enriched_transactions if t.get("API_Match"))

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("SALES ANALYTICS REPORT\n")
        f.write("=" * 40 + "\n\n")

        f.write("OVERALL SUMMARY\n")
        f.write("-" * 40 + "\n")
        f.write(f"Total Revenue: ₹{round(total_revenue, 2)}\n")
        f.write(f"Total Transactions: {total_transactions}\n")
        f.write(f"Average Order Value: ₹{round(avg_order_value, 2)}\n")
        f.write(f"Date Range: {date_range}\n\n")

        f.write("REGION WISE SALES\n")
        f.write("-" * 40 + "\n")
        for region, data in region_stats.items():
            f.write(
                f"{region}: ₹{round(data['total_sales'], 2)} "
                f"({round(data['percentage'], 2)}%), "
                f"Transactions: {data['transaction_count']}\n"
            )
        f.write("\n")

        f.write("TOP SELLING PRODUCTS\n")
        f.write("-" * 40 + "\n")
        for i, (name, qty, revenue) in enumerate(top_products, 1):
            f.write(f"{i}. {name} | Quantity: {qty} | Revenue: ₹{round(revenue, 2)}\n")
        f.write("\n")

        f.write("TOP CUSTOMERS\n")
        f.write("-" * 40 + "\n")
        for i, (cust, data) in enumerate(customers.items(), 1):
            if i > 5:
                break
            f.write(
                f"{i}. {cust} | Total Spent: ₹{round(data['total_spent'], 2)} "
                f"| Orders: {data['purchase_count']}\n"
            )
        f.write("\n")

        f.write("DAILY SALES TREND (first 10 days)\n")
        f.write("-" * 40 + "\n")
        for d, v in list(daily_trend.items())[:10]:
            f.write(
                f"{d}: Revenue ₹{round(v['revenue'], 2)}, "
                f"Transactions {v['transaction_count']}, "
                f"Customers {v['unique_customers']}\n"
            )
        f.write("\n")

        f.write("PEAK SALES DAY\n")
        f.write("-" * 40 + "\n")
        if peak_day:
            f.write(
                f"Date: {peak_day[0]}, "
                f"Revenue: ₹{round(peak_day[1], 2)}, "
                f"Transactions: {peak_day[2]}\n"
            )
        else:
            f.write("No data available\n")
        f.write("\n")

        f.write("API ENRICHMENT SUMMARY\n")
        f.write("-" * 40 + "\n")
        f.write(f"Enriched Transactions: {enriched_count} / {total_transactions}\n")

        f.write("\nReport generated on: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    return output_file
