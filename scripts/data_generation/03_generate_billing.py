import pandas as pd
import numpy as np
from datetime import date
from dateutil.relativedelta import relativedelta

def generate_billing_data(customers_file, output_file):
    """
    Generates 12 months of billing data for each customer.
    """
    try:
        customers_df = pd.read_csv(customers_file)
    except FileNotFoundError:
        print(f"Error: Customer file not found at {customers_file}")
        return

    num_customers = len(customers_df)
    num_records = num_customers * 12
    print(f"Generating {num_records} billing records for {num_customers} customers...")

    # Create 12 records for each customer by repeating their data
    billing_df = pd.DataFrame(np.repeat(customers_df.values, 12, axis=0), columns=customers_df.columns)

    # Generate BillingMonth for the last 12 months
    months = [(date.today() - relativedelta(months=i)).strftime('%Y-%m') for i in range(12, 0, -1)]
    billing_df['BillingMonth'] = np.tile(months, num_customers)

    # Generate unique BillingID
    billing_df['BillingID'] = [f'BILL-{i:07d}' for i in range(1, num_records + 1)]

    # Correlate MonthlyBill with MonthlyCharges, adding some noise
    billing_df['MonthlyCharges'] = pd.to_numeric(billing_df['MonthlyCharges'])
    noise = np.random.normal(0, billing_df['MonthlyCharges'].std() * 0.05, size=num_records)
    billing_df['MonthlyBill'] = (billing_df['MonthlyCharges'] + noise).round(2)

    # Tax, Discount, LateFee
    tax_rate = np.random.uniform(0.05, 0.12, size=num_records)
    billing_df['Tax'] = (billing_df['MonthlyBill'] * tax_rate).round(2)
    
    # Apply discount to 20% of bills
    discount_mask = np.random.choice([True, False], size=num_records, p=[0.2, 0.8])
    billing_df['Discount'] = np.where(discount_mask, (billing_df['MonthlyBill'] * np.random.uniform(0.05, 0.15, size=num_records)).round(2), 0)

    # Apply late fee to 10% of bills
    late_fee_mask = np.random.choice([True, False], size=num_records, p=[0.1, 0.9])
    billing_df['LateFee'] = np.where(late_fee_mask, (billing_df['MonthlyBill'] * np.random.uniform(0.02, 0.05, size=num_records)).round(2), 0)
    
    # Payment Status and Outstanding Amount
    status_choices = ['Paid', 'Paid Late', 'Pending']
    conditions = [
        billing_df['LateFee'] > 0,
        (billing_df['LateFee'] == 0) & (np.random.rand(num_records) < 0.95)
    ]
    outcomes = ['Paid Late', 'Paid']
    billing_df['PaymentStatus'] = np.select(conditions, outcomes, default='Pending')

    # Outstanding Amount should be 0 unless payment is Pending
    billing_df['TotalDue'] = billing_df['MonthlyBill'] + billing_df['Tax'] + billing_df['LateFee'] - billing_df['Discount']
    billing_df['OutstandingAmount'] = np.where(billing_df['PaymentStatus'] == 'Pending', billing_df['TotalDue'], 0)
    billing_df['OutstandingAmount'] = billing_df['OutstandingAmount'].clip(lower=0).round(2)

    # Select and order final columns
    final_columns = [
        'BillingID', 'customerID', 'BillingMonth', 'MonthlyBill',
        'Tax', 'Discount', 'LateFee', 'OutstandingAmount', 'PaymentStatus'
    ]
    final_df = billing_df[final_columns].copy()

    # Save to CSV
    final_df.to_csv(output_file, index=False)
    print(f"Successfully generated and saved {len(final_df)} records to {output_file}")


if __name__ == "__main__":
    customers_file_path = 'datasets/source/customers.csv'
    billing_output_file_path = 'datasets/source/billing.csv'
    
    generate_billing_data(customers_file_path, billing_output_file_path)
