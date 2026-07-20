import pandas as pd

file_path = "data/raw/customer_support_tickets.csv"

df = pd.read_csv(file_path)

print("=" * 60)
print("First 5 Rows")
print("=" * 60)
print(df.head())

print("\n")

print("=" * 60)
print("Dataset Shape")
print("=" * 60)
print(df.shape)

print("\n")

print("=" * 60)
print("Column Names")
print("=" * 60)
print(df.columns)

print("\n")

print("=" * 60)
print("Dataset Information")
print("=" * 60)
print(df.info())

print("\n")

print("=" * 60)
print("Statistical Summary")
print("=" * 60)
print(df.describe())

print("\n")

print("=" * 60)
print("Missing Values")
print("=" * 60)
print(df.isnull().sum())

print("\n")

print("=" * 60)
print("Duplicate Rows")
print("=" * 60)
print(df.duplicated().sum())