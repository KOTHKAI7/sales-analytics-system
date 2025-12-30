def read_sales_data(filepath):
    records = []
    with open(filepath, "r", encoding="latin-1") as f:
        header = f.readline().strip().split("|")
        for line in f:
            line = line.strip()
            if not line:
                continue
            values = line.split("|")
            if len(values) != len(header):
                continue
            record = dict(zip(header, values))
            records.append(record)
    return records
