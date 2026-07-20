import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Load cleaned dataset
df = pd.read_csv("data/processed/cleaned_data.csv")

# Drop unnecessary columns
drop_columns = [
    "ticket_id",
    "customer_name",
    "customer_email",
    "issue_description",
    "resolution_notes",
    "ticket_created_date",
    "ticket_resolved_date"
]

df = df.drop(columns=drop_columns)

# Encode categorical columns
encoders = {}

for col in df.select_dtypes(include="object").columns:
    encoder = LabelEncoder()
    df[col] = encoder.fit_transform(df[col].astype(str))
    encoders[col] = encoder

# Features
X = df.drop("priority", axis=1)

# Target
y = df["priority"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Train model
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)

# Prediction
predictions = model.predict(X_test)

print("\nAccuracy:")
print(accuracy_score(y_test, predictions))

print("\nClassification Report:")
print(classification_report(y_test, predictions))

# Save model
joblib.dump(model, "models/random_forest.pkl")
joblib.dump(encoders, "models/encoders.pkl")

print("\nModel Saved Successfully!")