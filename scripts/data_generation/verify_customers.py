import pandas as pd
import os

file_path = 'datasets/source/customers.csv'
try:
    df = pd.read_csv(file_path)

    row_count = len(df)
    col_count = len(df.columns)
    duplicate_customer_id_count = df['customerID'].duplicated().sum()
    null_value_count = df.isnull().sum().sum()

    print(f"customers.csv")
    print(f"Rows: {row_count}")
    print(f"Columns: {col_count}")
    print(f"Duplicate CustomerID: {duplicate_customer_id_count}")
    print(f"Null Values: {null_value_count}")


    if row_count == 20000 and col_count == 21 and duplicate_customer_id_count == 0:
        print("Status: PASSED")
    else:
        print("Status: FAILED")

except FileNotFoundError:
    print(f"Error: Verification failed. File not found at {file_path}")
