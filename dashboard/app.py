import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

from utils import load_data, kpis, filter_dataframe

st.set_page_config(
    page_title="AI Customer Support Intelligence Platform",
    page_icon="🤖",
    layout="wide"
)

df = load_data()

st.title("🤖 AI Customer Support Intelligence Platform")
st.caption("Interactive Dashboard for Customer Support Analytics")

# ==========================
# Sidebar
# ==========================

st.sidebar.header("Filters")

priority = st.sidebar.multiselect(
    "Priority",
    sorted(df["priority"].unique()),
    default=sorted(df["priority"].unique())
)

category = st.sidebar.multiselect(
    "Category",
    sorted(df["category"].unique()),
    default=sorted(df["category"].unique())
)

status = st.sidebar.multiselect(
    "Status",
    sorted(df["status"].unique()),
    default=sorted(df["status"].unique())
)

region = st.sidebar.multiselect(
    "Region",
    sorted(df["region"].unique()),
    default=sorted(df["region"].unique())
)

segment = st.sidebar.multiselect(
    "Customer Segment",
    sorted(df["customer_segment"].unique()),
    default=sorted(df["customer_segment"].unique())
)

df = filter_dataframe(
    df,
    priority,
    category,
    status,
    region,
    segment
)

# ==========================
# KPI CARDS
# ==========================

metrics = kpis(df)

c1,c2,c3,c4 = st.columns(4)

c1.metric(
    "Total Tickets",
    metrics["Total Tickets"]
)

c2.metric(
    "Avg Satisfaction",
    metrics["Average Satisfaction"]
)

c3.metric(
    "Avg Resolution",
    metrics["Average Resolution Time"]
)

c4.metric(
    "Avg First Response",
    metrics["Average First Response"]
)

c5,c6,c7,c8 = st.columns(4)

c5.metric(
    "Escalated",
    metrics["Escalated Tickets"]
)

c6.metric(
    "SLA Breached",
    metrics["SLA Breached"]
)

c7.metric(
    "Open",
    metrics["Open Tickets"]
)

c8.metric(
    "Closed",
    metrics["Closed Tickets"]
)

st.divider()

# ==========================
# PRIORITY
# ==========================

fig = px.histogram(
    df,
    x="priority",
    color="priority",
    title="Priority Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================
# STATUS
# ==========================

fig = px.histogram(
    df,
    x="status",
    color="status",
    title="Ticket Status"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================
# CATEGORY
# ==========================

fig = px.histogram(
    df,
    x="category",
    color="category",
    title="Issue Categories"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================
# REGION
# ==========================

fig = px.bar(
    df.groupby("region").size().reset_index(name="Tickets"),
    x="region",
    y="Tickets",
    color="region",
    title="Region-wise Tickets"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================
# PRODUCT
# ==========================

fig = px.bar(
    df.groupby("product").size().reset_index(name="Tickets"),
    x="product",
    y="Tickets",
    color="product",
    title="Product Analysis"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================
# CUSTOMER SEGMENT
# ==========================

fig = px.pie(
    df,
    names="customer_segment",
    title="Customer Segment"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
# ==========================
# SATISFACTION
# ==========================

st.subheader("⭐ Customer Satisfaction")

fig = px.histogram(
    df,
    x="customer_satisfaction_score",
    nbins=10,
    title="Customer Satisfaction Distribution"
)

st.plotly_chart(fig, use_container_width=True)

# ==========================
# RESPONSE VS RESOLUTION
# ==========================

st.subheader("⏱ Response vs Resolution Time")

fig = px.scatter(
    df,
    x="first_response_time_hours",
    y="resolution_time_hours",
    color="priority",
    hover_data=[
        "product",
        "category",
        "region"
    ]
)

st.plotly_chart(fig, use_container_width=True)

# ==========================
# MONTHLY TREND
# ==========================

st.subheader("📈 Monthly Ticket Trend")

monthly = (
    df.groupby(df["ticket_created_date"].dt.to_period("M"))
    .size()
    .reset_index(name="Tickets")
)

monthly["ticket_created_date"] = monthly["ticket_created_date"].astype(str)

fig = px.line(
    monthly,
    x="ticket_created_date",
    y="Tickets",
    markers=True
)

st.plotly_chart(fig, use_container_width=True)

# ==========================
# HEATMAP
# ==========================

st.subheader("🔥 Correlation Heatmap")

numeric = df.select_dtypes(include="number")

corr = numeric.corr().round(2)

fig = ff.create_annotated_heatmap(
    z=corr.values,
    x=list(corr.columns),
    y=list(corr.index),
    annotation_text=corr.values.astype(str),
    showscale=True
)

st.plotly_chart(fig, use_container_width=True)

# ==========================
# TOP INSIGHTS
# ==========================

st.subheader("🤖 AI Business Insights")

col1, col2 = st.columns(2)

with col1:

    st.success(
        f"Top Complaint Category : {df['category'].value_counts().idxmax()}"
    )

    st.success(
        f"Top Region : {df['region'].value_counts().idxmax()}"
    )

    st.success(
        f"Most Used Channel : {df['channel'].value_counts().idxmax()}"
    )

with col2:

    st.info(
        f"Highest Satisfaction Product : {df.groupby('product')['customer_satisfaction_score'].mean().idxmax()}"
    )

    st.info(
        f"Longest Resolution Category : {df.groupby('category')['resolution_time_hours'].mean().idxmax()}"
    )

    st.info(
        f"Average Satisfaction : {round(df['customer_satisfaction_score'].mean(),2)}"
    )

# ==========================
# SEARCH
# ==========================

st.subheader("🔍 Search Ticket")

ticket = st.text_input("Enter Ticket ID")

if ticket:

    result = df[df["ticket_id"].astype(str) == ticket]

    if len(result):

        st.dataframe(result, use_container_width=True)

    else:

        st.warning("Ticket Not Found")

# ==========================
# DOWNLOAD
# ==========================

st.subheader("⬇ Download Data")

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    "Download CSV",
    csv,
    file_name="customer_support_filtered.csv",
    mime="text/csv"
)

# ==========================
# DATASET
# ==========================

st.subheader("📋 Dataset")

st.dataframe(
    df,
    use_container_width=True,
    height=500
)

st.markdown("---")

st.caption(
    "AI Customer Support Intelligence Platform | Built with Streamlit, Pandas, Plotly & Scikit-Learn"
)