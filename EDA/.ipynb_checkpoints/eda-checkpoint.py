import pandas as pd

# -----------------------------------------
# 📊 CUSTOMER BEHAVIOR
# -----------------------------------------

def customer_behavior(df):

    print("\n📊 CUSTOMER BEHAVIOR\n")

    # 1. Churn %
    churn_pct = df['churn'].value_counts(normalize=True) * 100
    print("Churn Percentage:\n", churn_pct, "\n")

    # 2. Contract type churn
    contract_churn = pd.crosstab(df['contract_type'], df['churn'], normalize='index') * 100
    print("Churn by Contract Type (%):\n", contract_churn, "\n")

    # 3. Tenure vs churn
    tenure_churn = df.groupby('churn')['tenure'].mean()
    print("Average Tenure by Churn:\n", tenure_churn, "\n")

    # 4. Monthly charges vs churn
    charges_churn = df.groupby('churn')['monthly_charges'].mean()
    print("Average Monthly Charges by Churn:\n", charges_churn, "\n")


# -----------------------------------------
# 👥 DEMOGRAPHICS
# -----------------------------------------

def demographics(df):

    print("\n👥 DEMOGRAPHICS\n")

    # 1. Gender churn
    gender_churn = pd.crosstab(df['gender'], df['churn'], normalize='index') * 100
    print("Churn by Gender (%):\n", gender_churn, "\n")

    # 2. Age group churn
    df['age_group'] = pd.cut(
        df['age'],
        bins=[0, 25, 40, 60, 100],
        labels=['Young', 'Adult', 'Mid-Age', 'Senior']
    )

    age_churn = pd.crosstab(df['age_group'], df['churn'], normalize='index') * 100
    print("Churn by Age Group (%):\n", age_churn, "\n")


# -----------------------------------------
# 💰 REVENUE IMPACT
# -----------------------------------------

def revenue_impact(df):

    print("\n💰 REVENUE IMPACT\n")

    # 1. Revenue lost
    revenue_lost = df[df['churn'] == 'Yes']['total_charges'].sum()
    print("Total Revenue Lost due to Churn:", revenue_lost, "\n")

    # 2. Monthly charges comparison
    monthly_compare = df.groupby('churn')['monthly_charges'].mean()
    print("Avg Monthly Charges (Churn vs Non-Churn):\n", monthly_compare, "\n")


# -----------------------------------------
# 🌐 SERVICES
# -----------------------------------------

def services_analysis(df):

    print("\n🌐 SERVICES\n")

    # 1. Internet service churn
    internet_churn = pd.crosstab(df['internet_service'], df['churn'], normalize='index') * 100
    print("Churn by Internet Service (%):\n", internet_churn, "\n")

    # 2. Payment method churn
    payment_churn = pd.crosstab(df['payment_method'], df['churn'], normalize='index') * 100
    print("Churn by Payment Method (%):\n", payment_churn, "\n")


# -----------------------------------------
# 🚀 MAIN FUNCTION
# -----------------------------------------

def run_eda(df):

    print("="*50)
    print("🚀 STARTING EDA")
    print("="*50)

    customer_behavior(df)
    demographics(df)
    revenue_impact(df)
    services_analysis(df)

    print("="*50)
    print("✅ EDA COMPLETED")
    print("="*50)