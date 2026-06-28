import pandas as pd

def verify_cdr_data(cdr_file, customers_file):
    """
    Verifies the generated CDR dataset.
    """
    print("--- CDR Data Verification ---")
    try:
        cdr_df = pd.read_csv(cdr_file, dtype={'CustomerID': str})
        customers_df = pd.read_csv(customers_file, dtype={'CustomerID': str})
    except FileNotFoundError as e:
        print(f"Error: Could not find file {e.filename}")
        print("Status: FAILED")
        return

    # 1. Row Count
    row_count = len(cdr_df)
    print(f"Row Count: {row_count} (Expected: 300,000)")
    if row_count != 300000:
        print("Status: FAILED - Incorrect row count.")
        return

    # 2. Duplicate Primary Keys (CallID)
    duplicate_pks = cdr_df['CallID'].duplicated().sum()
    print(f"Duplicate CallIDs: {duplicate_pks} (Expected: 0)")
    if duplicate_pks > 0:
        print("Status: FAILED - Found duplicate CallIDs.")
        return

    # 3. Invalid CustomerIDs
    customer_ids = set(customers_df['customerID'])
    invalid_customer_ids = cdr_df[~cdr_df['CustomerID'].isin(customer_ids)]
    print(f"Invalid CustomerIDs: {len(invalid_customer_ids)} (Expected: 0)")
    if len(invalid_customer_ids) > 0:
        print("Status: FAILED - Found CustomerIDs not present in the master customers file.")
        return

    # 4. Null Values
    # 4. Null Values
    null_values = cdr_df.isnull().sum().sum()
    print(f"Null Values: {null_values} (Expected: 0)")
    if null_values > 0:
        print("Columns with nulls:")
        print(cdr_df.isnull().sum()[cdr_df.isnull().sum() > 0])
        print("Status: FAILED - Found null values.")
        return

    # 5. Data Types
    print("Data Types Check:")
    print(cdr_df.dtypes)

    # Simple check for date/time formats, assuming they are strings
    try:
        pd.to_datetime(cdr_df['CallDate'])
        print("- CallDate format: OK")
    except Exception as e:
        print(f"- CallDate format: FAILED ({e})")
        return

    print("\nStatus: PASSED")
    print("--------------------------")


if __name__ == "__main__":
    verify_cdr_data('datasets/source/cdr.csv', 'datasets/source/customers.csv')
