import pandas as pd

def load_data():
    df = pd.read_csv("data/processed/cleaned_data.csv")

    df["ticket_created_date"] = pd.to_datetime(df["ticket_created_date"])
    df["ticket_resolved_date"] = pd.to_datetime(df["ticket_resolved_date"])

    return df


def kpis(df):
    return {
        "Total Tickets": len(df),
        "Average Satisfaction": round(df["customer_satisfaction_score"].mean(), 2),
        "Average Resolution Time": round(df["resolution_time_hours"].mean(), 2),
        "Average First Response": round(df["first_response_time_hours"].mean(), 2),
        "Escalated Tickets": (df["escalated"] == "Yes").sum(),
        "SLA Breached": (df["sla_breached"] == "Yes").sum(),
        "Open Tickets": (df["status"] == "Open").sum(),
        "Closed Tickets": (df["status"] == "Closed").sum()
    }


def filter_dataframe(
    df,
    priority,
    category,
    status,
    region,
    segment
):
    return df[
        (df["priority"].isin(priority)) &
        (df["category"].isin(category)) &
        (df["status"].isin(status)) &
        (df["region"].isin(region)) &
        (df["customer_segment"].isin(segment))
    ]