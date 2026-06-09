import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from scoring import calculate_scores
from ai_agent import generate_recommendation
from database import (
    create_table,
    insert_log,
    get_logs_dataframe
)

# Create database
create_table()

# Page Configuration
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
st.sidebar.success("✅ Vendor Comparison")
st.sidebar.success("✅ Risk Detection")
st.sidebar.success("✅ Procurement Savings")
st.sidebar.success("✅ Negotiation Opportunities")
st.sidebar.success("✅ Explainable AI")
st.sidebar.success("✅ Audit Logs")
st.sidebar.success("✅ Dashboard Analytics")

# Upload CSV
uploaded_file = st.file_uploader(
    "Upload Vendor Quotation CSV",
    type=["csv"]
)

if uploaded_file:

    # Read CSV
    df = pd.read_csv(uploaded_file)

    st.subheader("Uploaded Vendor Quotations")
    st.dataframe(df)

    st.markdown("---")

    # Calculate Scores
    scored_df = calculate_scores(df)

    st.subheader("Vendor Ranking Dashboard")
    st.dataframe(scored_df)

    st.subheader("🥇 Top 3 Vendors")

    top3 = scored_df.head(3)[
        ["Vendor", "Score", "Risk_Level"]
    ]

    st.dataframe(top3)

    # Download Report
    st.download_button(
        label="📥 Download Procurement Report",
        data=scored_df.to_csv(index=False),
        file_name="procurement_report.csv",
        mime="text/csv"
    )

    st.markdown("---")

    # Best Vendor
    best_vendor = scored_df.iloc[0]["Vendor"]
    best_score = scored_df.iloc[0]["Score"]

    st.success(
        f"🏆 Best Vendor Selected: {best_vendor}"
    )

    # Recommendation Card
    winner = scored_df.iloc[0]

    st.success(
        f"""
📌 Vendor Recommendation

Vendor: {winner['Vendor']}

Price: ₹{winner['Price']}

Delivery Days: {winner['Delivery_Days']}

Warranty: {winner['Warranty_Years']} Years

Support Rating: {winner['Support_Rating']}/10

Reason:
Best balance of cost, delivery speed,
warranty support and vendor reliability.
"""
    )

    # Save Audit Log
    insert_log(
        best_vendor,
        float(best_score)
    )

    st.markdown("---")

    # Vendor Comparison
    st.subheader("⚖️ Vendor Comparison")

    vendor_list = scored_df["Vendor"].tolist()

    if len(vendor_list) >= 2:

        vendor1 = st.selectbox(
            "Select Vendor 1",
            vendor_list
        )

        vendor2 = st.selectbox(
            "Select Vendor 2",
            vendor_list,
            index=1
        )

        compare_df = scored_df[
            scored_df["Vendor"].isin(
                [vendor1, vendor2]
            )
        ]

        st.dataframe(compare_df)

    st.markdown("---")

    st.subheader("🔍 Search Vendor")

    search_vendor = st.selectbox(
        "Select Vendor",
        scored_df["Vendor"]
    )

    vendor_info = scored_df[
        scored_df["Vendor"] == search_vendor
    ]

    st.dataframe(vendor_info)

    st.markdown("---")

    # KPI Dashboard
    st.subheader("📊 Procurement KPI Dashboard")

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

    avg_score = round(
        scored_df["Score"].mean(),
        2
    )

    st.metric(
        "Overall Procurement Health",
        f"{avg_score}%"
    )

    # Procurement Savings
    max_price = scored_df["Price"].max()

    best_price = scored_df.iloc[0]["Price"]

    savings = max_price - best_price

    st.metric(
        "Estimated Savings",
        f"₹{savings:,.0f}"
    )

    st.subheader("📌 Project Statistics")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Average Score",
        round(scored_df["Score"].mean(), 2)
    )

    col2.metric(
        "Highest Price",
        f"₹{scored_df['Price'].max():,.0f}"
    )

    col3.metric(
        "Lowest Price",
        f"₹{scored_df['Price'].min():,.0f}"
    )

    # Health Status
    if avg_score > 50:

        st.success(
            "🟢 Procurement Health: Excellent"
        )

    elif avg_score > 35:

        st.warning(
            "🟡 Procurement Health: Moderate"
        )

    else:

        st.error(
            "🔴 Procurement Health: Poor"
        )

    st.markdown("---")

    # Risk Detection
    st.subheader("⚠️ Procurement Risk Detection")

    for _, row in scored_df.iterrows():

        if row["Delivery_Days"] > 15:

            st.error(
                f"{row['Vendor']} has HIGH delivery delay risk."
            )

        elif row["Price"] > 54000:

            st.warning(
                f"{row['Vendor']} quotation price is expensive."
            )

        else:

            st.success(
                f"{row['Vendor']} risk level is acceptable."
            )

    st.subheader("📊 Risk Summary")

    risk_counts = scored_df["Risk_Level"].value_counts()

    st.dataframe(
        risk_counts.reset_index().rename(
            columns={
                "index": "Risk Level",
                "Risk_Level": "Count"
            }
        )
    )


    st.markdown("---")

    # Negotiation Opportunities
    st.subheader("💰 Negotiation Opportunities")

    for _, row in scored_df.iterrows():

        if row["Price"] > 55000:

            st.warning(
                f"{row['Vendor']} quotation is expensive. Recommended negotiation target."
            )

    st.markdown("---")

    # Bar Chart
    st.subheader("📈 Vendor Score Visualization")

    fig, ax = plt.subplots(figsize=(10, 4))

    bars = ax.bar(
        scored_df["Vendor"],
        scored_df["Score"]
    )

    ax.set_title(
        "Vendor Score Comparison",
        fontsize=14,
        fontweight="bold"
    )

    ax.set_xlabel("Vendors")
    ax.set_ylabel("Score")

    plt.xticks(
        rotation=45,
        ha="right"
    )

    plt.tight_layout()

    st.pyplot(fig)

    st.subheader("🏆 Top Vendor Ranking")

    top_vendors = scored_df.head(10)

    fig3, ax3 = plt.subplots(figsize=(8, 4))

    ax3.barh(
        top_vendors["Vendor"],
        top_vendors["Score"]
    )

    ax3.set_xlabel("Score")
    ax3.set_ylabel("Vendor")

    ax3.set_title(
        "Top Vendor Ranking"
    )

    plt.tight_layout()

    st.pyplot(fig3)

    st.markdown("---")

    # AI Insights
    st.subheader("🤖 AI Procurement Insights")

    recommendation = generate_recommendation(
        scored_df.to_string()
    )

    st.write(recommendation)

    st.markdown("---")

    # Explainability
    st.subheader("Why This Vendor Was Selected")

    st.write(
        f"""
{best_vendor} achieved the highest procurement score based on pricing efficiency, delivery speed, warranty quality, and support services.
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
AI analysis identified that vendors with lower pricing often provide slower delivery timelines, while premium vendors offer stronger warranty support and customer service.
"""
    )

    st.markdown("---")

    # Summary
    st.subheader("Procurement Summary")

    st.write(
        f"""
SmartProcure AI analyzed {len(scored_df)} vendors and selected **{best_vendor}** as the most suitable procurement partner based on pricing, delivery efficiency, warranty support, and vendor quality metrics.
"""
    )

    st.markdown("---")

    # Audit Logs
    st.subheader("📋 Procurement Audit Logs")

    logs_df = get_logs_dataframe()

    if not logs_df.empty:
        st.dataframe(logs_df)
    else:
        st.info(
            "No audit logs available."
        )

else:

    st.warning(
        "Please upload a vendor quotation CSV file to begin analysis."
    )