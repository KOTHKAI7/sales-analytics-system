# utils/data_processor.py

from collections import defaultdict
from datetime import datetime


# =========================
# PART 1.2 — PARSE & CLEAN
# =========================

def parse_transactions(raw_lines):
    """
    Parses raw pipe-delimited lines into cleaned list of dictionaries.
    Skips rows with incorrect number of fields.
    Handles commas in ProductName and numeric fields.
    """

    transactions = []

    for line in raw_lines:
        parts = line.split("|")
        if len(parts) != 8:
            continue  # skip malformed rows

        try:
            transaction_id, date, product_id, product_name, quantity, unit_price, customer_id, region = parts

            product_name = product_name.replace(",", "")
            quantity = int(quantity.replace(",", ""))
            unit_price = float(unit_price.replace(",", ""))

            transactions.append({
                "TransactionID": transaction_id.strip(),
                "Date": date.strip(),
                "ProductID": product_id.strip(),
                "ProductName": product_name.strip(),
                "Quantity": quantity,
                "UnitPrice": unit_price,
                "CustomerID": customer_id.strip(),
                "Region": region.strip()
            })

        except Exception:
            continue

    return transactions


# ==============================
# PART 1.3 — VALIDATE & FILTER
# ==============================

def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    Validates transactions and applies optional filters.
    Returns (valid_transactions, invalid_count, summary_dict)
    """

    valid = []
    invalid = 0
    summary = {
        "total_input": len(transactions),
        "invalid": 0,
        "filtered_by_region": 0,
        "filtered_by_amount": 0,
        "final_count": 0
    }

    for t in transactions:
        try:
            if not t["TransactionID"].startswith("T"):
                invalid += 1
                continue
            if not t["ProductID"].startswith("P"):
                invalid += 1
                continue
            if not t["CustomerID"].startswith("C"):
                invalid += 1
                continue
            if t["Quantity"] <= 0 or t["UnitPrice"] <= 0:
                invalid += 1
                continue

            amount = t["Quantity"] * t["UnitPrice"]

            if region and t["Region"].lower() != region.lower():
                summary["filtered_by_region"] += 1
                continue

            if min_amount is not None and amount < min_amount:
                summary["filtered_by_amount"] += 1
                continue

            if max_amount is not None and amount > max_amount:
                summary["filtered_by_amount"] += 1
                continue

            valid.append(t)

        except Exception:
            invalid += 1

    summary["invalid"] = invalid
    summary["final_count"] = len(valid)

    return valid, invalid, summary


# =========================
# PART 2.1 — TOTAL REVENUE
# =========================

def calculate_total_revenue(transactions):
    return sum(t["Quantity"] * t["UnitPrice"] for t in transactions)


# =========================
# PART 2.1 — REGION SALES
# =========================

def region_wise_sales(transactions):
    revenue = defaultdict(float)
    count = defaultdict(int)
    total = calculate_total_revenue(transactions)

    for t in transactions:
        revenue[t["Region"]] += t["Quantity"] * t["UnitPrice"]
        count[t["Region"]] += 1

    result = {}
    for r in revenue:
        result[r] = {
            "total_sales": revenue[r],
            "transaction_count": count[r],
            "percentage": (revenue[r] / total * 100) if total else 0
        }

    return dict(sorted(result.items(), key=lambda x: x[1]["total_sales"], reverse=True))


# =========================
# PART 2.1 — TOP PRODUCTS
# =========================

def top_selling_products(transactions, n=5):
    products = defaultdict(lambda: {"qty": 0, "revenue": 0})

    for t in transactions:
        name = t["ProductName"]
        products[name]["qty"] += t["Quantity"]
        products[name]["revenue"] += t["Quantity"] * t["UnitPrice"]

    ranked = [(k, v["qty"], v["revenue"]) for k, v in products.items()]
    ranked.sort(key=lambda x: x[1], reverse=True)

    return ranked[:n]


# =========================
# PART 2.1 — CUSTOMER ANALYSIS
# =========================

def customer_analysis(transactions):
    customers = defaultdict(lambda: {"spent": 0, "count": 0, "products": set()})

    for t in transactions:
        c = t["CustomerID"]
        amt = t["Quantity"] * t["UnitPrice"]
        customers[c]["spent"] += amt
        customers[c]["count"] += 1
        customers[c]["products"].add(t["ProductName"])

    result = {}
    for c, v in customers.items():
        result[c] = {
            "total_spent": v["spent"],
            "purchase_count": v["count"],
            "avg_order_value": v["spent"] / v["count"],
            "products_bought": sorted(list(v["products"]))
        }

    return dict(sorted(result.items(), key=lambda x: x[1]["total_spent"], reverse=True))


# =========================
# PART 2.2 — DAILY TREND
# =========================

def daily_sales_trend(transactions):
    trend = defaultdict(lambda: {"revenue": 0, "count": 0, "customers": set()})

    for t in transactions:
        d = t["Date"]
        trend[d]["revenue"] += t["Quantity"] * t["UnitPrice"]
        trend[d]["count"] += 1
        trend[d]["customers"].add(t["CustomerID"])

    result = {}
    for d in sorted(trend.keys(), key=lambda x: datetime.strptime(x, "%Y-%m-%d")):
        result[d] = {
            "revenue": trend[d]["revenue"],
            "transaction_count": trend[d]["count"],
            "unique_customers": len(trend[d]["customers"])
        }

    return result


def find_peak_sales_day(transactions):
    trend = daily_sales_trend(transactions)
    if not trend:
        return None

    day = max(trend.items(), key=lambda x: x[1]["revenue"])
    return (day[0], day[1]["revenue"], day[1]["transaction_count"])


# =========================
# PART 2.3 — LOW PRODUCTS
# =========================

def low_performing_products(transactions, threshold=10):
    products = defaultdict(lambda: {"qty": 0, "revenue": 0})

    for t in transactions:
        products[t["ProductName"]]["qty"] += t["Quantity"]
        products[t["ProductName"]]["revenue"] += t["Quantity"] * t["UnitPrice"]

    low = [(k, v["qty"], v["revenue"]) for k, v in products.items() if v["qty"] < threshold]
    low.sort(key=lambda x: x[1])

    return low
