def clean_sales_data(records):
    valid = []
    invalid = 0

    for r in records:
        try:
            if not r["TransactionID"].startswith("T"):
                invalid += 1
                continue

            if not r["CustomerID"] or not r["Region"]:
                invalid += 1
                continue

            qty = int(r["Quantity"])
            price = float(r["UnitPrice"].replace(",", ""))

            if qty <= 0 or price <= 0:
                invalid += 1
                continue

            r["Quantity"] = qty
            r["UnitPrice"] = price
            r["ProductName"] = r["ProductName"].replace(",", "")

            valid.append(r)

        except:
            invalid += 1

    print(f"Total records parsed: {len(records)}")
    print(f"Invalid records removed: {invalid}")
    print(f"Valid records after cleaning: {len(valid)}")

    return valid
