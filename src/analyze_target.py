import pandas as pd

df = pd.read_csv("data/processed/cleaned_data.csv")

print(df["priority"].value_counts())
print()
print(df["priority"].value_counts(normalize=True) * 100)