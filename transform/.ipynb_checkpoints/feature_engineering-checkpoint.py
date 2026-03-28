import numpy as np

def create_realistic_churn(df):

    np.random.seed(42)

    churn_prob = np.full(len(df), 0.2)

    churn_prob += np.where(df['contract_type'] == 'Month-To-Month', 0.25, 0)
    churn_prob -= np.where(df['contract_type'] == 'Two Year', 0.15, 0)

    churn_prob += np.where(df['tenure'] < 12, 0.2, 0)
    churn_prob -= np.where(df['tenure'] > 36, 0.1, 0)

    churn_prob += np.where(df['monthly_charges'] > 80, 0.15, 0)

    churn_prob += np.where(df['internet_service'] == 'Fiber Optic', 0.1, 0)

    churn_prob -= np.where(df['payment_method'].isin(['Credit Card', 'Debit Card']), 0.1, 0)

    churn_prob = np.clip(churn_prob, 0, 1)

    df['churn'] = np.where(np.random.rand(len(df)) < churn_prob, 'Yes', 'No')

    return df