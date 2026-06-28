
import pandas as pd

def verify_customer_feedback_data(customer_feedback_file, customers_file):
    """
    Verifies the integrity of the generated customer feedback data.
    """
    print(f"Verifying {customer_feedback_file}...")
    
    try:
        customer_feedback_df = pd.read_csv(customer_feedback_file)
        customers_df = pd.read_csv(customers_file)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return

    # 1. Row count
    required_rows = 20000
    if len(customer_feedback_df) == required_rows:
        print(f"[PASS] Row count is correct ({required_rows}).")
    else:
        print(f"[FAIL] Row count is incorrect. Expected {required_rows}, got {len(customer_feedback_df)}.")

    # 2. Column count
    required_columns = ['feedback_id', 'customerID', 'submission_date', 'rating_score', 'feedback_text']
    if all(col in customer_feedback_df.columns for col in required_columns) and len(customer_feedback_df.columns) == len(required_columns):
        print(f"[PASS] Column count and names are correct.")
    else:
        print(f"[FAIL] Columns are incorrect. Expected {required_columns}, got {list(customer_feedback_df.columns)}.")

    # 3. Duplicate primary keys
    if customer_feedback_df['feedback_id'].is_unique:
        print("[PASS] No duplicate primary keys (feedback_id).")
    else:
        print(f"[FAIL] Found duplicate primary keys (feedback_id).")

    # 4. Invalid CustomerIDs
    valid_customer_ids = set(customers_df['customerID'])
    invalid_customer_ids = customer_feedback_df[~customer_feedback_df['customerID'].isin(valid_customer_ids)]
    if len(invalid_customer_ids) == 0:
        print("[PASS] All CustomerIDs are valid.")
    else:
        print(f"[FAIL] Found {len(invalid_customer_ids)} invalid CustomerIDs.")

    # 5. Null values
    if customer_feedback_df.isnull().sum().sum() == 0:
        print("[PASS] No null values found.")
    else:
        print(f"[FAIL] Found null values:")
        print(customer_feedback_df.isnull().sum())

if __name__ == "__main__":
    customer_feedback_file_path = 'datasets/source/customer_feedback.csv'
    customers_file_path = 'datasets/source/customers.csv'
    verify_customer_feedback_data(customer_feedback_file_path, customers_file_path)
