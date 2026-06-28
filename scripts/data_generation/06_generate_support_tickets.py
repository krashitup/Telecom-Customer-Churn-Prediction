
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_support_tickets_data(customers_file, output_file, num_rows):
    """
    Generates support ticket data for customers.
    """
    try:
        customers_df = pd.read_csv(customers_file)
    except FileNotFoundError:
        print(f"Error: Customer file not found at {customers_file}")
        return

    print(f"Generating {num_rows} support ticket records...")

    customer_ids = np.random.choice(customers_df['customerID'], size=num_rows, replace=True)
    ticket_ids = [f'TKT-{i:07d}' for i in range(1, num_rows + 1)]

    # Generate ticket dates within the last 12 months
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    open_dates = [start_date + timedelta(seconds=np.random.randint(0, int((end_date - start_date).total_seconds()))) for _ in range(num_rows)]

    # Resolution time: 1 hour to 14 days
    resolution_times = np.random.randint(3600, 14 * 24 * 3600, size=num_rows)
    
    status_choices = ['Closed', 'Open', 'Pending Customer']
    statuses = np.random.choice(status_choices, size=num_rows, p=[0.8, 0.1, 0.1])

    close_dates = []
    for i in range(num_rows):
        if statuses[i] == 'Closed':
            close_dates.append((open_dates[i] + timedelta(seconds=int(resolution_times[i]))).strftime('%Y-%m-%d'))
        else:
            close_dates.append(None) # No close date if not closed

    issue_types = np.random.choice(
        ['Billing Inquiry', 'Service Interruption', 'Technical Support', 'New Service Request', 'Cancellation Request'],
        size=num_rows,
        p=[0.3, 0.25, 0.25, 0.1, 0.1]
    )
    priorities = np.random.choice(['Low', 'Medium', 'High'], size=num_rows, p=[0.5, 0.3, 0.2])

    # Create DataFrame
    support_tickets_df = pd.DataFrame({
        'ticket_id': ticket_ids,
        'customerID': customer_ids,
        'ticket_open_date': [d.strftime('%Y-%m-%d') for d in open_dates],
        'ticket_close_date': close_dates,
        'issue_type': issue_types,
        'priority': priorities,
        'status': statuses
    })

    # Save to CSV
    support_tickets_df.to_csv(output_file, index=False)
    print(f"Successfully generated and saved {len(support_tickets_df)} records to {output_file}")


if __name__ == "__main__":
    customers_file_path = 'datasets/source/customers.csv'
    support_tickets_output_file_path = 'datasets/source/support_tickets.csv'
    total_support_tickets_rows = 30000

    generate_support_tickets_data(customers_file_path, support_tickets_output_file_path, total_support_tickets_rows)
