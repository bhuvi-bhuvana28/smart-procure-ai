import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from scoring import calculate_scores
from ai_agent import generate_recommendation
from database import create_table, insert_log

# Create DB table
create_table()

# Page Config
st.set_page_config(
    page_title="SmartProcure AI",
    layout="wide"
)

# Header
st.title("SmartProcure AI")

st.subheader(
    "AI-Powered Procurement Intelligence System"
)

st.markdown("---")

# Sidebar
st.sidebar.title("Features")

st.sidebar.write("✅ Vendor Ranking")
st.sidebar.write("✅ AI Negotiation")
st.sidebar.write("✅ Risk Detection")
st.sidebar.write("✅ Explainable AI")
st.sidebar.write("✅ Audit Logs")

# Upload CSV
uploaded_file = st.file_uploader(
    "Upload Vendor Quotation CSV",
    type=["csv"]
)

if uploaded_file:

    # Read file
    df = pd.read_csv(uploaded_file)

    st.subheader("Uploaded Vendor Quotations")

    st.dataframe(df)

    st.markdown("---")

    # Score calculation
    scored_df = calculate_scores(df)

    st.subheader("Vendor Ranking Dashboard")

    st.dataframe(scored_df)

     # Best Vendor
    best_vendor = scored_df.iloc[0]["Vendor"]

    best_score = scored_df.iloc[0]["Score"]

    st.success(
        f"Best Vendor Selected: {best_vendor}"
    )

    # Insert audit log
    insert_log(best_vendor, best_score)

    # Risk Detection
    st.subheader("Procurement Risk Meter")

    for _, row in scored_df.iterrows():

        if row["Delivery_Days"] > 15:
            st.error(
                f"⚠️ {row['Vendor']} has high delivery risk"
            )

        elif row["Price"] > 54000:
            st.warning(
                f"⚠️ {row['Vendor']} quotation is expensive"
            )

        else:
            st.success(
                f"✅ {row['Vendor']} risk level is acceptable"
            )

    st.markdown(
    "### Intelligent AI Procurement Decision System"
)

    # Chart
    st.subheader("Vendor Score Visualization")

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.bar(
        scored_df["Vendor"],
        scored_df["Score"]
    )

    ax.set_ylabel("Vendor Score")

    ax.set_title("Vendor Comparison")

    st.pyplot(fig)

    st.markdown("---")

    # AI Recommendation
    st.subheader("AI Procurement Insights")

    with st.spinner(
        "Generating AI procurement insights..."
    ):

        recommendation = generate_recommendation(
            scored_df.to_string()
        )

        st.write(recommendation)

    st.markdown("---")

    st.subheader("Explainable AI Decision")

    st.info(
        "Vendor ranking is calculated based on price, delivery speed, warranty, and support quality using weighted scoring."
    )

else:

    st.info(
        "Upload a CSV file to start procurement analysis."
    )