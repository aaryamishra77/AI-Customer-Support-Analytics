import streamlit as st
import pandas as pd
import os


st.set_page_config(
    page_title="Ticket Search",
    page_icon="🔎",
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



st.title("🔎 Customer Support Ticket Search")



search = st.text_input(
    "Search ticket, customer or issue"
)



priority = st.multiselect(
    "Priority",
    df["priority"].unique()
)



status = st.multiselect(
    "Status",
    df["status"].unique()
)



result = df.copy()



if search:

    result = result[
        result.astype(str)
        .apply(
            lambda row:
            row.str.contains(
                search,
                case=False
            ).any(),
            axis=1
        )
    ]



if priority:

    result = result[
        result["priority"]
        .isin(priority)
    ]



if status:

    result = result[
        result["status"]
        .isin(status)
    ]



st.write(
    f"Found {len(result)} tickets"
)



st.dataframe(
    result,
    use_container_width=True
)



if len(result)>0:


    st.subheader(
        "🎫 Ticket Details"
    )


    ticket = st.selectbox(
        "Select Ticket ID",
        result["ticket_id"]
    )


    details = result[
        result["ticket_id"]==ticket
    ].iloc[0]



    st.write(details)



    csv = details.to_frame().T.to_csv(
        index=False
    )


    st.download_button(
        "Download Ticket",
        csv,
        "ticket.csv"
    )