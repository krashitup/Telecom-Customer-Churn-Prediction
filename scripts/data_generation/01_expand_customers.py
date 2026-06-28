import pandas as pd
import numpy as np
import os

def expand_customers(original_file_path, target_rows):
    """
    Expands the customer dataset to a target number of rows while preserving
    the statistical distribution of the original data.
    """
    try:
        df = pd.read_csv(original_file_path)
    except FileNotFoundError:
        print(f"Error: The file {original_file_path} was not found.")
        return

    original_rows = len(df)
    if original_rows >= target_rows:
        print(f"Dataset already has {original_rows} rows. No expansion needed.")
        df.to_csv(original_file_path, index=False)
        return

    num_new_rows = target_rows - original_rows

    # Create new data by sampling with replacement
    new_data = df.sample(n=num_new_rows, replace=True, random_state=42)

    # Generate new unique customer IDs
    existing_ids = set(df['customerID'])
    new_ids = []
    i = 0
    while len(new_ids) < num_new_rows:
        new_id = f'GEN-{i:05}'
        if new_id not in existing_ids:
            new_ids.append(new_id)
        i += 1
    new_data['customerID'] = new_ids

    # Add noise to numeric columns to ensure new rows are not exact duplicates
    numeric_cols = new_data.select_dtypes(include=np.number).columns
    for col in numeric_cols:
        std = df[col].std()
        noise = np.random.normal(0, std * 0.1, size=num_new_rows)
        new_data[col] += noise
        if col in ['tenure', 'MonthlyCharges', 'TotalCharges']:
             new_data[col] = new_data[col].clip(lower=0)

    # Clean 'TotalCharges' column and round 'tenure'
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    new_data['TotalCharges'] = pd.to_numeric(new_data['TotalCharges'], errors='coerce')
    new_data['tenure'] = new_data['tenure'].round().astype(int)

    # Concatenate old and new dataframes
    expanded_df = pd.concat([df, new_data], ignore_index=True)

    # Save the result
    expanded_df.to_csv(original_file_path, index=False)
    print(f"Successfully expanded dataset to {len(expanded_df)} rows.")

if __name__ == "__main__":
    file_path = 'datasets/source/customers.csv'
    target_count = 20000
    expand_customers(file_path, target_count)
