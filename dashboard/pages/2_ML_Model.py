import streamlit as st
import pandas as pd
import numpy as np
import os

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix

import plotly.express as px


st.set_page_config(
    page_title="ML Model",
    page_icon="🧠",
    layout="wide"
)


def load_data():

    BASE_DIR = os.path.dirname(
        os.path.dirname(
            os.path.dirname(__file__)
        )
    )

    DATA_PATH = os.path.join(
        BASE_DIR,
        "data",
        "raw",
        "customer_support_tickets.csv"
    )

    return pd.read_csv(DATA_PATH)



df = load_data()


st.title("🧠 Ticket Priority Prediction Model")


st.success(
    f"Dataset Loaded Successfully: {df.shape[0]} rows"
)


with st.expander("View Dataset Preview"):

    st.dataframe(
        df.head(),
        use_container_width=True
    )



features = [

    "customer_age",
    "customer_tenure_months",
    "previous_tickets",
    "customer_satisfaction_score",
    "first_response_time_hours",
    "resolution_time_hours",
    "issue_complexity_score"

]


target = "priority"



missing = []

for col in features + [target]:

    if col not in df.columns:
        missing.append(col)



if missing:

    st.error(
        f"Missing columns in dataset: {missing}"
    )

    st.stop()



data = df[
    features + [target]
].dropna()



st.info(
    f"Training Data: {data.shape[0]} records"
)



X = data[features]

y = data[target]



encoder = LabelEncoder()


y_encoded = encoder.fit_transform(
    y
)



X_train, X_test, y_train, y_test = train_test_split(

    X,
    y_encoded,
    test_size=0.2,
    random_state=42

)



with st.spinner("Training Machine Learning Model..."):


    model = RandomForestClassifier(

        n_estimators=50,
        random_state=42,
        n_jobs=-1

    )


    model.fit(
        X_train,
        y_train
    )



prediction = model.predict(
    X_test
)



accuracy = accuracy_score(
    y_test,
    prediction
)



st.success(
    f"Model Accuracy: {accuracy*100:.2f}%"
)



st.divider()


st.subheader("📊 Confusion Matrix")



cm = confusion_matrix(
    y_test,
    prediction
)



fig = px.imshow(

    cm,

    text_auto=True,

    labels={

        "x":"Predicted",

        "y":"Actual"

    }

)



st.plotly_chart(

    fig,

    use_container_width=True

)



st.divider()


st.subheader("🔥 Feature Importance")



importance = pd.DataFrame(

    {

        "Feature": features,

        "Importance":
        model.feature_importances_

    }

)



importance = importance.sort_values(

    by="Importance",

    ascending=False

)



fig2 = px.bar(

    importance,

    x="Importance",

    y="Feature",

    orientation="h"

)



st.plotly_chart(

    fig2,

    use_container_width=True

)



st.divider()


st.subheader("🎯 Predict New Ticket Priority")



col1, col2, col3 = st.columns(3)



inputs = {}



with col1:

    inputs["customer_age"] = st.number_input(
        "Customer Age",
        25
    )


    inputs["customer_tenure_months"] = st.number_input(
        "Customer Tenure Months",
        12
    )


    inputs["previous_tickets"] = st.number_input(
        "Previous Tickets",
        2
    )



with col2:

    inputs["customer_satisfaction_score"] = st.slider(
        "Satisfaction Score",
        1,
        5,
        3
    )


    inputs["first_response_time_hours"] = st.number_input(
        "First Response Time",
        5.0
    )



with col3:

    inputs["resolution_time_hours"] = st.number_input(
        "Resolution Time",
        10.0
    )


    inputs["issue_complexity_score"] = st.slider(
        "Issue Complexity",
        1,
        10,
        5
    )



if st.button("Predict Priority"):


    input_df = pd.DataFrame(

        [inputs]

    )


    result = model.predict(
        input_df
    )


    priority = encoder.inverse_transform(
        result
    )[0]


    st.success(
        f"Predicted Ticket Priority: {priority}"
    )