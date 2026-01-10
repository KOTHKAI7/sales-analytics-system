# utils/api_handler.py

import requests

BASE_URL = "https://dummyjson.com/products"


# PART 3.1 — FETCH PRODUCTS

def fetch_all_products():
    try:
        response = requests.get(BASE_URL, timeout=6)
        response.raise_for_status()
        data = response.json()

        # DummyJSON returns {"products": [...], "total": X}
        products = data.get("products", [])
        print(f" Fetched {len(products)} products from API")
        return products

    except Exception as e:
        print("✗ API fetch failed:", e)
        return []


# PART 3.1 — CREATE PRODUCT MAPPING

def create_product_mapping(api_products):
  
    mapping = {}

    for p in api_products:
        try:
            pid = int(p.get("id"))
            mapping[pid] = {
                "title": p.get("title"),
                "category": p.get("category"),
                "brand": p.get("brand"),
                "rating": p.get("rating")
            }
        except Exception:
            continue

    return mapping


# PART 3.2 — ENRICH SALES DATA

def enrich_sales_data(transactions, product_mapping):
    """
    Enriches transactions with API product info.
    Adds API_Category, API_Brand, API_Rating, API_Match.
    Returns (enriched_transactions, stats)
    """

    enriched = []
    success = 0
    failed_products = set()

    for t in transactions:
        record = t.copy()
        pid = str(t.get("ProductID", "")).strip()

        try:
            # P101 -> 101
            numeric_id = int(pid.replace("P", ""))
        except Exception:
            numeric_id = None

        api_data = product_mapping.get(numeric_id)

        if api_data:
            record["API_Category"] = api_data["category"]
            record["API_Brand"] = api_data["brand"]
            record["API_Rating"] = api_data["rating"]
            record["API_Match"] = True
            success += 1
        else:
            record["API_Category"] = None
            record["API_Brand"] = None
            record["API_Rating"] = None
            record["API_Match"] = False
            failed_products.add(pid)

        enriched.append(record)

    stats = {
        "total": len(transactions),
        "enriched": success,
        "success_rate": (success / len(transactions) * 100) if transactions else 0,
        "failed_products": sorted(list(failed_products))
    }

    return enriched, stats


# PART 3.2 — SAVE ENRICHED DATA FILE

def save_enriched_data(enriched_transactions, filename="data/enriched_sales_data.txt"):
    """
    Saves enriched transactions to a pipe-delimited file.
    """

    header = [
        "TransactionID", "Date", "ProductID", "ProductName",
        "Quantity", "UnitPrice", "CustomerID", "Region",
        "API_Category", "API_Brand", "API_Rating", "API_Match"
    ]

    with open(filename, "w", encoding="utf-8") as f:
        f.write("|".join(header) + "\n")

        for t in enriched_transactions:
            row = [
                str(t.get("TransactionID", "")),
                str(t.get("Date", "")),
                str(t.get("ProductID", "")),
                str(t.get("ProductName", "")).replace("|", " "),
                str(t.get("Quantity", "")),
                str(t.get("UnitPrice", "")),
                str(t.get("CustomerID", "")),
                str(t.get("Region", "")),
                str(t.get("API_Category") or ""),
                str(t.get("API_Brand") or ""),
                str(t.get("API_Rating") or ""),
                str(t.get("API_Match"))
            ]
            f.write("|".join(row) + "\n")

    return filename
