
import pandas as pd

def verify_support_tickets_data(support_tickets_file, customers_file):
    """
    Verifies the integrity of the generated support tickets data.
    """
    print(f"Verifying {support_tickets_file}...")
    
    try:
        support_tickets_df = pd.read_csv(support_tickets_file)
        customers_df = pd.read_csv(customers_file)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return

    # 1. Row count
    required_rows = 30000
    if len(support_tickets_df) == required_rows:
        print(f"[PASS] Row count is correct ({required_rows}).")
    else:
        print(f"[FAIL] Row count is incorrect. Expected {required_rows}, got {len(support_tickets_df)}.")

    # 2. Column count
    required_columns = ['ticket_id', 'customerID', 'ticket_open_date', 'ticket_close_date', 'issue_type', 'priority', 'status']
    if all(col in support_tickets_df.columns for col in required_columns) and len(support_tickets_df.columns) == len(required_columns):
        print(f"[PASS] Column count and names are correct.")
    else:
        print(f"[FAIL] Columns are incorrect. Expected {required_columns}, got {list(support_tickets_df.columns)}.")

    # 3. Duplicate primary keys
    if support_tickets_df['ticket_id'].is_unique:
        print("[PASS] No duplicate primary keys (ticket_id).")
    else:
        print(f"[FAIL] Found duplicate primary keys (ticket_id).")

    # 4. Invalid CustomerIDs
    valid_customer_ids = set(customers_df['customerID'])
    invalid_customer_ids = support_tickets_df[~support_tickets_df['customerID'].isin(valid_customer_ids)]
    if len(invalid_customer_ids) == 0:
        print("[PASS] All CustomerIDs are valid.")
    else:
        print(f"[FAIL] Found {len(invalid_customer_ids)} invalid CustomerIDs.")

    # 5. Null values
    # Allow nulls in 'ticket_close_date'
    cols_to_check = support_tickets_df.columns.drop('ticket_close_date')
    if support_tickets_df[cols_to_check].isnull().sum().sum() == 0:
        print("[PASS] No unexpected null values found.")
    else:
        print(f"[FAIL] Found unexpected null values:")
        print(support_tickets_df[cols_to_check].isnull().sum())

if __name__ == "__main__":
    support_tickets_file_path = 'datasets/source/support_tickets.csv'
    customers_file_path = 'datasets/source/customers.csv'
    verify_support_tickets_data(support_tickets_file_path, customers_file_path)
