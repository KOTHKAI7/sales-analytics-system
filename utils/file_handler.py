def read_sales_data(filename):
    """
    Reads sales data from file handling encoding issues.
    Returns list of raw transaction lines (strings).
    """

    encodings_to_try = ["utf-8", "latin-1", "cp1252"]
    last_error = None

    for enc in encodings_to_try:
        try:
            with open(filename, "r", encoding=enc) as f:
                lines = f.readlines()

            # Remove header
            if lines:
                lines = lines[1:]

            # Remove empty lines and strip newline characters
            cleaned_lines = [line.strip() for line in lines if line.strip()]
            return cleaned_lines

        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {filename}")

        except Exception as e:
            last_error = e
            continue

    raise Exception(f"Failed to read file due to encoding issues: {last_error}")
