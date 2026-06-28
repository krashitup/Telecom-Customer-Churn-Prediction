import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_cdr_data(customers_file, output_file, num_rows):
    """
    Generates Call Detail Records (CDR) for customers.
    """
    try:
        customers_df = pd.read_csv(customers_file)
    except FileNotFoundError:
        print(f"Error: Customer file not found at {customers_file}")
        return

    customer_ids = customers_df['customerID'].unique()
    
    # Ensure the number of rows is exactly as requested
    print(f"Generating {num_rows} call records...")
    cdr_customer_ids = np.random.choice(customer_ids, size=num_rows, replace=True)

    # Generate data
    call_ids = [f'CALL-{i:07d}' for i in range(1, num_rows + 1)]
    
    # Dates within the last 12 months
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    call_datetimes = [start_date + timedelta(seconds=np.random.randint(0, int((end_date - start_date).total_seconds()))) for _ in range(num_rows)]
    
    call_dates = [d.date() for d in call_datetimes]
    call_start_times = [d.time().strftime('%H:%M:%S') for d in call_datetimes]
    
    # Call duration: 10 seconds to 2 hours
    call_durations = np.random.randint(10, 7201, size=num_rows)
    
    call_end_times = [(datetime.combine(call_datetimes[i].date(), datetime.min.time()) + timedelta(seconds=int(call_datetimes[i].hour*3600 + call_datetimes[i].minute*60 + call_datetimes[i].second + call_durations[i]))).time().strftime('%H:%M:%S') for i in range(num_rows)]
    
    call_types = np.random.choice(['Voice', 'Video'], size=num_rows, p=[0.8, 0.2])
    
    # Dropped calls: 3-8%
    dropped_rate = np.random.uniform(0.03, 0.08)
    dropped_calls = np.random.choice([True, False], size=num_rows, p=[dropped_rate, 1 - dropped_rate])
    
    # Tower IDs
    tower_ids = [f'TWR-{i:03d}' for i in range(1, 101)]
    assigned_tower_ids = np.random.choice(tower_ids, size=num_rows)
    
    # Network Type - link to internet service
    customer_internet_service = customers_df.set_index('customerID')['InternetService'].to_dict()
    network_types = []
    for cid in cdr_customer_ids:
        service = customer_internet_service.get(cid)
        if service == 'Fiber optic':
            network_types.append(np.random.choice(['5G', '4G'], p=[0.7, 0.3]))
        else: # DSL or No
            network_types.append(np.random.choice(['4G', '5G'], p=[0.9, 0.1]))

    # Create DataFrame
    cdr_df = pd.DataFrame({
        'CallID': call_ids,
        'CustomerID': cdr_customer_ids,
        'CallDate': call_dates,
        'CallStartTime': call_start_times,
        'CallEndTime': call_end_times,
        'CallDuration': call_durations,
        'CallType': call_types,
        'DroppedCall': dropped_calls,
        'TowerID': assigned_tower_ids,
        'NetworkType': network_types
    })

    # Save to CSV, overwriting the existing file
    cdr_df.to_csv(output_file, index=False)
    print(f"Successfully generated and saved {len(cdr_df)} records to {output_file}")


if __name__ == "__main__":
    customers_file_path = 'datasets/source/customers.csv'
    cdr_output_file_path = 'datasets/source/cdr.csv'
    total_cdr_rows = 300000
    
    generate_cdr_data(customers_file_path, cdr_output_file_path, total_cdr_rows)
