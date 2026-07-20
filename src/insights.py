import pandas as pd

df = pd.read_csv("data/processed/cleaned_data.csv")

print("\n========== AI BUSINESS INSIGHTS ==========\n")

print("Top Category:")
print(df["category"].value_counts().idxmax())

print("\nTop Region:")
print(df["region"].value_counts().idxmax())

print("\nMost Used Channel:")
print(df["channel"].value_counts().idxmax())

print("\nHighest Satisfaction:")
print(df.groupby("product")["customer_satisfaction_score"].mean().idxmax())

print("\nLongest Resolution:")
print(df.groupby("category")["resolution_time_hours"].mean().idxmax())