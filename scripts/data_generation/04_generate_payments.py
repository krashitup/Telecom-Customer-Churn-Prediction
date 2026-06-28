
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_payments_data(billing_file, output_file, num_rows):
    """
    Generates payment data based on billing records.
    """
    try:
        billing_df = pd.read_csv(billing_file)
    except FileNotFoundError:
        print(f"Error: Billing file not found at {billing_file}")
        return

    # If billing_df is larger than num_rows, sample it. Otherwise, sample with replacement.
    if len(billing_df) >= num_rows:
        billing_subset = billing_df.sample(n=num_rows, replace=False)
    else:
        billing_subset = billing_df.sample(n=num_rows, replace=True)

    print(f"Generating {num_rows} payment records...")

    payment_ids = [f'PAY-{i:07d}' for i in range(1, num_rows + 1)]
    
    # Generate payment dates around the billing month
    payment_dates = []
    for month_str in billing_subset['BillingMonth']:
        billing_month = datetime.strptime(month_str + '-01', '%Y-%m-%d')
        payment_day = np.random.randint(1, 28)
        payment_date = billing_month + timedelta(days=payment_day - 1)
        payment_dates.append(payment_date.strftime('%Y-%m-%d'))

    payment_methods = np.random.choice(
        ['Credit card (automatic)', 'Bank transfer (automatic)', 'Mailed check', 'Electronic check'],
        size=num_rows,
        p=[0.4, 0.3, 0.1, 0.2]
    )
    
    # Base amount on billing components, with some variation
    billing_subset['TotalDue'] = billing_subset['MonthlyBill'] + billing_subset['Tax'] + billing_subset['LateFee'] - billing_subset['Discount']
    amounts = (billing_subset['TotalDue'] * np.random.uniform(0.95, 1.05)).round(2)

    # Payment status
    status_choices = ['Completed', 'Failed', 'Pending']
    # Link status to outstanding amount from billing
    conditions = [
        billing_subset['OutstandingAmount'] == 0, # Paid
        billing_subset['PaymentStatus'] == 'Pending'
    ]
    outcomes = ['Completed', 'Pending']
    status = np.select(conditions, outcomes, default='Failed') # Default to Failed if not clearly paid or pending

    # Create DataFrame
    payments_df = pd.DataFrame({
        'payment_id': payment_ids,
        'customerID': billing_subset['customerID'],
        'payment_date': payment_dates,
        'amount': amounts,
        'payment_method': payment_methods,
        'status': status
    })

    # Save to CSV
    payments_df.to_csv(output_file, index=False)
    print(f"Successfully generated and saved {len(payments_df)} records to {output_file}")


if __name__ == "__main__":
    billing_file_path = 'datasets/source/billing.csv'
    payments_output_file_path = 'datasets/source/payments.csv'
    total_payments_rows = 240000
    
    generate_payments_data(billing_file_path, payments_output_file_path, total_payments_rows)
