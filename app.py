import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from scoring import calculate_scores
from ai_agent import generate_recommendation
from database import create_table, insert_log

# Create database
create_table()

# Page Config
st.set_page_config(
    page_title="SmartProcure AI",
    layout="wide"
)

# Title
st.title("SmartProcure AI")

st.markdown(
    "## AI-Powered Procurement Intelligence System"
)

st.info(
    "SmartProcure AI helps enterprises automate vendor evaluation, procurement analysis, risk detection, and negotiation planning using Artificial Intelligence."
)

st.markdown("---")

# Sidebar
st.sidebar.title("Features")

st.sidebar.success("✅ Vendor Ranking")
st.sidebar.success("✅ AI Negotiation")
st.sidebar.success("✅ Risk Detection")
st.sidebar.success("✅ Explainable AI")
st.sidebar.success("✅ Audit Logs")
st.sidebar.success("✅ Dashboard Analytics")

# Upload CSV
uploaded_file = st.file_uploader(
    "Upload Vendor Quotation CSV",
    type=["csv"]
)

# If file uploaded
if uploaded_file:

    # Read CSV
    df = pd.read_csv(uploaded_file)

    st.subheader("Uploaded Vendor Quotations")

    st.dataframe(df)

    st.markdown("---")

    # Calculate scores
    scored_df = calculate_scores(df)

    st.subheader("Vendor Ranking Dashboard")

    st.dataframe(scored_df)

    # Best Vendor
    best_vendor = scored_df.iloc[0]["Vendor"]

    best_score = scored_df.iloc[0]["Score"]

    st.success(
        f"🏆 Best Vendor Selected: {best_vendor}"
    )

    # Save log
    insert_log(best_vendor, best_score)

    st.markdown("---")

    # KPI Cards
    st.subheader("Procurement KPI Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Vendors",
        len(scored_df)
    )

    col2.metric(
        "Best Vendor",
        best_vendor
    )

    col3.metric(
        "Highest Score",
        round(best_score, 2)
    )

    st.markdown("---")

    # Risk Detection
    st.subheader("Procurement Risk Detection")

    for _, row in scored_df.iterrows():

        if row["Delivery_Days"] > 15:

            st.error(
                f"⚠️ {row['Vendor']} has HIGH delivery delay risk."
            )

        elif row["Price"] > 54000:

            st.warning(
                f"⚠️ {row['Vendor']} quotation price is expensive."
            )

        else:

            st.success(
                f"✅ {row['Vendor']} risk level is acceptable."
            )

    st.markdown("---")

    # Bar Chart
    st.subheader("Vendor Score Visualization")

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.bar(
        scored_df["Vendor"],
        scored_df["Score"]
    )

    ax.set_xlabel("Vendors")

    ax.set_ylabel("Scores")

    ax.set_title("Vendor Comparison Dashboard")

    st.pyplot(fig)

    st.markdown("---")

    # Pie Chart
    st.subheader("Vendor Score Distribution")

    fig2, ax2 = plt.subplots(figsize=(7, 7))

    ax2.pie(
        scored_df["Score"],
        labels=scored_df["Vendor"],
        autopct='%1.1f%%'
    )

    st.pyplot(fig2)

    st.markdown("---")

    # AI Insights
    st.subheader("AI Procurement Insights")

    with st.spinner(
        "Generating procurement insights..."
    ):

        recommendation = generate_recommendation(
            scored_df.to_string()
        )

        st.write(recommendation)

    st.markdown("---")

    # Explainability
    st.subheader("Why This Vendor Was Selected")

    st.write(
        f"""
        {best_vendor} achieved the highest procurement score
        based on delivery speed, pricing efficiency,
        warranty quality, and support services.
        """
    )

    st.markdown("---")

    # Explainable AI
    st.subheader("Explainable AI Decision")

    st.info(
        """
        Vendor scores are calculated using weighted procurement evaluation.

        Weight Distribution:
        • Price → 40%
        • Delivery Speed → 25%
        • Warranty → 20%
        • Support Quality → 15%

        This ensures transparent and explainable procurement decision-making.
        """
    )

    st.markdown("---")

    # Procurement Intelligence
    st.subheader("Procurement Intelligence")

    st.info(
        """
        AI analysis identified that vendors with lower pricing
        often provide slower delivery timelines, while premium vendors
        offer stronger warranty support and better customer service.
        """
    )

    st.markdown("---")

    # Final Summary
    st.subheader("Procurement Summary")

    st.write(
        f"""
        SmartProcure AI analyzed {len(scored_df)} vendors and selected
        **{best_vendor}** as the most suitable procurement partner
        based on pricing, delivery efficiency,
        warranty support, and vendor quality metrics.
        """
    )

else:

    st.warning(
        "Please upload a vendor quotation CSV file to begin analysis."
    )