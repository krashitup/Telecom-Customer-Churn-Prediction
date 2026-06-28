
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_internet_usage_data(customers_file, output_file, num_rows):
    """
    Generates internet usage data for customers.
    """
    try:
        customers_df = pd.read_csv(customers_file)
    except FileNotFoundError:
        print(f"Error: Customer file not found at {customers_file}")
        return
    
    # Only generate usage for customers with internet service
    internet_customers = customers_df[customers_df['InternetService'] != 'No']['customerID']
    
    if len(internet_customers) == 0:
        print("No customers with internet service found. Cannot generate usage data.")
        return

    print(f"Generating {num_rows} internet usage records...")

    # Sample customer IDs
    customer_ids = np.random.choice(internet_customers, size=num_rows, replace=True)

    usage_ids = [f'USAGE-{i:07d}' for i in range(1, num_rows + 1)]

    # Generate session times within the last 12 months
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    session_starts = [start_date + timedelta(seconds=np.random.randint(0, int((end_date - start_date).total_seconds()))) for _ in range(num_rows)]
    
    # Session duration: 5 minutes to 8 hours
    session_durations = np.random.randint(300, 28801, size=num_rows)
    session_ends = [session_starts[i] + timedelta(seconds=int(session_durations[i])) for i in range(num_rows)]

    # Data consumed in GB (proportional to session duration)
    data_consumed = (session_durations / 3600) * np.random.uniform(0.5, 3.0) # Assume 0.5-3.0 GB/hour
    data_consumed = np.round(data_consumed, 4)

    devices = np.random.choice(
        ['Desktop', 'Mobile', 'Tablet', 'Smart TV', 'Gaming Console'],
        size=num_rows,
        p=[0.3, 0.4, 0.15, 0.1, 0.05]
    )

    # Create DataFrame
    internet_usage_df = pd.DataFrame({
        'usage_id': usage_ids,
        'customerID': customer_ids,
        'session_start_time': [s.strftime('%Y-%m-%d %H:%M:%S') for s in session_starts],
        'session_end_time': [e.strftime('%Y-%m-%d %H:%M:%S') for e in session_ends],
        'data_consumed_gb': data_consumed,
        'device': devices
    })

    # Save to CSV
    internet_usage_df.to_csv(output_file, index=False)
    print(f"Successfully generated and saved {len(internet_usage_df)} records to {output_file}")


if __name__ == "__main__":
    customers_file_path = 'datasets/source/customers.csv'
    internet_usage_output_file_path = 'datasets/source/internet_usage.csv'
    total_internet_usage_rows = 240000

    generate_internet_usage_data(customers_file_path, internet_usage_output_file_path, total_internet_usage_rows)
