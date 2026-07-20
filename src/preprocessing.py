import pandas as pd

# Load dataset
df = pd.read_csv("data/raw/customer_support_tickets.csv")

print("Original Shape:", df.shape)

# Remove duplicate rows
df.drop_duplicates(inplace=True)

# Fill missing numeric values
numeric_columns = [
    "customer_satisfaction_score",
    "first_response_time_hours",
    "resolution_time_hours",
    "customer_age",
    "customer_tenure_months",
    "previous_tickets",
    "issue_complexity_score"
]

for col in numeric_columns:
    if col in df.columns:
        df[col] = df[col].fillna(df[col].median())

# Fill missing categorical values
categorical_columns = [
    "product",
    "category",
    "priority",
    "status",
    "channel",
    "region",
    "subscription_type",
    "customer_gender",
    "operating_system",
    "browser",
    "payment_method",
    "language",
    "preferred_contact_time",
    "customer_segment"
]

for col in categorical_columns:
    if col in df.columns:
        df[col] = df[col].fillna(df[col].mode()[0])

print("\nMissing Values:")
print(df.isnull().sum())

# Save cleaned dataset
df.to_csv("data/processed/cleaned_data.csv", index=False)

print("\n✅ Cleaned dataset saved successfully!")