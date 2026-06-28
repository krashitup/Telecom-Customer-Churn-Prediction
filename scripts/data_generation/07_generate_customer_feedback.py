
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_customer_feedback_data(customers_file, output_file):
    """
    Generates customer feedback data. One feedback entry per customer.
    """
    try:
        customers_df = pd.read_csv(customers_file)
    except FileNotFoundError:
        print(f"Error: Customer file not found at {customers_file}")
        return

    num_customers = len(customers_df)
    print(f"Generating {num_customers} customer feedback records...")

    customer_ids = customers_df['customerID']
    feedback_ids = [f'FB-{i:07d}' for i in range(1, num_customers + 1)]

    # Generate submission dates within the last 12 months
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    submission_dates = [start_date + timedelta(seconds=np.random.randint(0, int((end_date - start_date).total_seconds()))) for _ in range(num_customers)]

    # Generate ratings (1-5)
    rating_scores = np.random.randint(1, 6, size=num_customers)

    # Generate feedback text based on rating
    feedback_texts = []
    for rating in rating_scores:
        if rating == 5:
            feedback_texts.append(np.random.choice([
                "Excellent service, very satisfied!",
                "Great experience, no issues.",
                "Fast and reliable, highly recommend."
            ]))
        elif rating == 4:
            feedback_texts.append(np.random.choice([
                "Good service, but could be slightly faster.",
                "Mostly positive experience.",
                "Happy with the service overall."
            ]))
        elif rating == 3:
            feedback_texts.append(np.random.choice([
                "Service is average. Room for improvement.",
                "It's okay, but not great.",
                "Had a few minor issues."
            ]))
        elif rating == 2:
            feedback_texts.append(np.random.choice([
                "Poor experience, frequent disconnects.",
                "Not happy with the service.",
                "Customer support was not helpful."
            ]))
        else: # rating == 1
            feedback_texts.append(np.random.choice([
                "Very poor service, would not recommend.",
                "Constantly having problems.",
                "Extremely dissatisfied."
            ]))

    # Create DataFrame
    customer_feedback_df = pd.DataFrame({
        'feedback_id': feedback_ids,
        'customerID': customer_ids,
        'submission_date': [d.strftime('%Y-%m-%d') for d in submission_dates],
        'rating_score': rating_scores,
        'feedback_text': feedback_texts
    })

    # Save to CSV
    customer_feedback_df.to_csv(output_file, index=False)
    print(f"Successfully generated and saved {len(customer_feedback_df)} records to {output_file}")


if __name__ == "__main__":
    customers_file_path = 'datasets/source/customers.csv'
    customer_feedback_output_file_path = 'datasets/source/customer_feedback.csv'
    
    generate_customer_feedback_data(customers_file_path, customer_feedback_output_file_path)
