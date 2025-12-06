from ocr_utils import (
    analyze_document,
    print_basic_debug,
    extract_plain_text,
    extract_tables,
    extract_key_value_pairs,
)

def main():
    file_path = "./dummy_statement.pdf"  # or sample_bank_statement.pdf

    # Choose model: 'prebuilt-layout' for structure, 'prebuilt-document' for KV
    model_id = "prebuilt-layout"

    print(f"Analyzing file: {file_path} with model: {model_id}")
    result = analyze_document(file_path, model_id=model_id)

    # Quick debug print
    print_basic_debug(result)

    # If you want to use the structured data programmatically:
    text = extract_plain_text(result)
    kv = extract_key_value_pairs(result)
    tables = extract_tables(result)

    print("\n=== Programmatic Usage Demo ===")
    print(f"\nTotal characters in plain text: {len(text)}")

    print("\nAvailable KV keys:", list(kv.keys()))

    print("\nTable count:", len(tables))
    if tables:
        print("First row of first table:", tables[0][0])


if __name__ == "__main__":
    main()
