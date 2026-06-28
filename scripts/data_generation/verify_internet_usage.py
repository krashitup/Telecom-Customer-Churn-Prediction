
import pandas as pd

def verify_internet_usage_data(internet_usage_file, customers_file):
    """
    Verifies the integrity of the generated internet usage data.
    """
    print(f"Verifying {internet_usage_file}...")
    
    try:
        internet_usage_df = pd.read_csv(internet_usage_file)
        customers_df = pd.read_csv(customers_file)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return

    # 1. Row count
    required_rows = 240000
    if len(internet_usage_df) == required_rows:
        print(f"[PASS] Row count is correct ({required_rows}).")
    else:
        print(f"[FAIL] Row count is incorrect. Expected {required_rows}, got {len(internet_usage_df)}.")

    # 2. Column count
    required_columns = ['usage_id', 'customerID', 'session_start_time', 'session_end_time', 'data_consumed_gb', 'device']
    if all(col in internet_usage_df.columns for col in required_columns) and len(internet_usage_df.columns) == len(required_columns):
        print(f"[PASS] Column count and names are correct.")
    else:
        print(f"[FAIL] Columns are incorrect. Expected {required_columns}, got {list(internet_usage_df.columns)}.")

    # 3. Duplicate primary keys
    if internet_usage_df['usage_id'].is_unique:
        print("[PASS] No duplicate primary keys (usage_id).")
    else:
        print(f"[FAIL] Found duplicate primary keys (usage_id).")

    # 4. Invalid CustomerIDs
    valid_customer_ids = set(customers_df['customerID'])
    invalid_customer_ids = internet_usage_df[~internet_usage_df['customerID'].isin(valid_customer_ids)]
    if len(invalid_customer_ids) == 0:
        print("[PASS] All CustomerIDs are valid.")
    else:
        print(f"[FAIL] Found {len(invalid_customer_ids)} invalid CustomerIDs.")

    # 5. Null values
    if internet_usage_df.isnull().sum().sum() == 0:
        print("[PASS] No null values found.")
    else:
        print(f"[FAIL] Found null values:")
        print(internet_usage_df.isnull().sum())

if __name__ == "__main__":
    internet_usage_file_path = 'datasets/source/internet_usage.csv'
    customers_file_path = 'datasets/source/customers.csv'
    verify_internet_usage_data(internet_usage_file_path, customers_file_path)
