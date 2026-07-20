import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv("data/raw/customer_support_tickets.csv")

# Plot style
sns.set_style("whitegrid")

# Priority Distribution
plt.figure(figsize=(8,5))

sns.countplot(data=df, x="priority")

plt.title("Ticket Priority Distribution")

plt.xlabel("Priority")

plt.ylabel("Number of Tickets")

plt.show()
plt.figure(figsize=(8,5))

sns.countplot(data=df, x="status")

plt.title("Ticket Status")

plt.xticks(rotation=20)

plt.show()
plt.figure(figsize=(8,5))

sns.countplot(data=df, x="customer_segment")

plt.title("Customer Segment")

plt.xticks(rotation=20)

plt.show()
plt.figure(figsize=(10,5))

sns.countplot(data=df, x="category")

plt.title("Issue Categories")

plt.xticks(rotation=45)

plt.show()