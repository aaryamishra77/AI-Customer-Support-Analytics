import streamlit as st
import pandas as pd
import plotly.express as px
import os


st.set_page_config(
    page_title="AI Insights",
    page_icon="🤖",
    layout="wide"
)


def load_data():

    BASE_DIR = os.path.dirname(
        os.path.dirname(
            os.path.dirname(__file__)
        )
    )

    path = os.path.join(
        BASE_DIR,
        "data",
        "raw",
        "customer_support_tickets.csv"
    )

    return pd.read_csv(path)



df = load_data()


st.title("🤖 AI Business Insights")

st.write(
    "AI-generated insights from customer support data"
)


col1, col2, col3 = st.columns(3)


with col1:
    st.metric(
        "Average Resolution Time",
        f"{df['resolution_time_hours'].mean():.2f} hrs"
    )


with col2:
    st.metric(
        "Average Response Time",
        f"{df['first_response_time_hours'].mean():.2f} hrs"
    )


with col3:
    st.metric(
        "Average Satisfaction",
        round(
            df["customer_satisfaction_score"].mean(),
            2
        )
    )


st.divider()


st.subheader("🚨 Priority Distribution")


priority = (
    df["priority"]
    .value_counts()
    .reset_index()
)


priority.columns = [
    "Priority",
    "Count"
]


fig = px.bar(
    priority,
    x="Priority",
    y="Count",
    text="Count"
)


st.plotly_chart(
    fig,
    use_container_width=True
)


st.subheader("💡 AI Recommendations")


urgent = len(
    df[df["priority"]=="Urgent"]
)


high = len(
    df[df["priority"]=="High"]
)


low_satisfaction = len(
    df[
        df["customer_satisfaction_score"] < 3
    ]
)


st.warning(
    f"""
Urgent Tickets: {urgent}

Actions:
- Prioritize urgent issues
- Enable escalation
- Increase agent attention
"""
)


st.info(
    f"""
High Priority Tickets: {high}

Actions:
- Monitor SLA
- Reduce response delays
"""
)


st.error(
    f"""
Low Satisfaction Customers: {low_satisfaction}

Actions:
- Improve resolution quality
- Follow up with customers
"""
)


st.divider()


st.subheader("📊 Category Resolution Analysis")


category = (
    df.groupby("category")
    ["resolution_time_hours"]
    .mean()
    .reset_index()
)


fig2 = px.bar(
    category,
    x="category",
    y="resolution_time_hours"
)


st.plotly_chart(
    fig2,
    use_container_width=True
)