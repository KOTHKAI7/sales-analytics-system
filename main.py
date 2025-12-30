from utils.file_handler import read_sales_data
from utils.data_processor import clean_sales_data

DATA_PATH = "data/sales_data.txt"

def generate_report(data):
    revenue = sum(r["Quantity"] * r["UnitPrice"] for r in data)
    print(f"Total Revenue: ₹{round(revenue, 2)}")

if __name__ == "__main__":
    records = read_sales_data(DATA_PATH)
    cleaned = clean_sales_data(records)
    generate_report(cleaned)
