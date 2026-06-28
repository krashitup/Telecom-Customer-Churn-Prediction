
import pandas as pd

def verify_payments_data(payments_file, customers_file):
    """
    Verifies the integrity of the generated payments data.
    """
    print(f"Verifying {payments_file}...")
    
    try:
        payments_df = pd.read_csv(payments_file)
        customers_df = pd.read_csv(customers_file)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return

    # 1. Row count
    required_rows = 240000
    if len(payments_df) == required_rows:
        print(f"[PASS] Row count is correct ({required_rows}).")
    else:
        print(f"[FAIL] Row count is incorrect. Expected {required_rows}, got {len(payments_df)}.")

    # 2. Column count
    required_columns = ['payment_id', 'customerID', 'payment_date', 'amount', 'payment_method', 'status']
    if all(col in payments_df.columns for col in required_columns) and len(payments_df.columns) == len(required_columns):
        print(f"[PASS] Column count and names are correct.")
    else:
        print(f"[FAIL] Columns are incorrect. Expected {required_columns}, got {list(payments_df.columns)}.")

    # 3. Duplicate primary keys
    if payments_df['payment_id'].is_unique:
        print("[PASS] No duplicate primary keys (payment_id).")
    else:
        print(f"[FAIL] Found duplicate primary keys (payment_id).")

    # 4. Invalid CustomerIDs
    valid_customer_ids = set(customers_df['customerID'])
    invalid_customer_ids = payments_df[~payments_df['customerID'].isin(valid_customer_ids)]
    if len(invalid_customer_ids) == 0:
        print("[PASS] All CustomerIDs are valid.")
    else:
        print(f"[FAIL] Found {len(invalid_customer_ids)} invalid CustomerIDs.")

    # 5. Null values
    if payments_df.isnull().sum().sum() == 0:
        print("[PASS] No null values found.")
    else:
        print(f"[FAIL] Found null values:")
        print(payments_df.isnull().sum())

if __name__ == "__main__":
    payments_file_path = 'datasets/source/payments.csv'
    customers_file_path = 'datasets/source/customers.csv'
    verify_payments_data(payments_file_path, customers_file_path)
