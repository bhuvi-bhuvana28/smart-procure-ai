import pandas as pd


def calculate_scores(df):

    # Convert columns to numeric
    df["Price"] = pd.to_numeric(
        df["Price"],
        errors="coerce"
    )

    df["Delivery_Days"] = pd.to_numeric(
        df["Delivery_Days"],
        errors="coerce"
    )

    df["Warranty_Years"] = pd.to_numeric(
        df["Warranty_Years"],
        errors="coerce"
    )

    df["Support_Rating"] = pd.to_numeric(
        df["Support_Rating"],
        errors="coerce"
    )

    # Remove invalid rows
    df = df.dropna()

    # Maximum values
    max_price = df["Price"].max()

    max_delivery = df["Delivery_Days"].max()

    max_warranty = df["Warranty_Years"].max()

    max_support = df["Support_Rating"].max()

    scores = []

    risk_levels = []

    for _, row in df.iterrows():

        # Price Score (Lower Price Better)
        price_score = (
            (max_price - row["Price"])
            / max_price
        ) * 40

        # Delivery Score (Faster Delivery Better)
        delivery_score = (
            (max_delivery - row["Delivery_Days"])
            / max_delivery
        ) * 25

        # Warranty Score
        warranty_score = (
            row["Warranty_Years"]
            / max_warranty
        ) * 20

        # Support Score
        support_score = (
            row["Support_Rating"]
            / max_support
        ) * 15

        total_score = (
            price_score +
            delivery_score +
            warranty_score +
            support_score
        )

        scores.append(
            round(total_score, 2)
        )

        # Risk Classification
        if row["Delivery_Days"] > 15:

            risk_levels.append(
                "High"
            )

        elif row["Price"] > 55000:

            risk_levels.append(
                "Medium"
            )

        else:

            risk_levels.append(
                "Low"
            )

    # Add columns
    df["Score"] = scores

    df["Risk_Level"] = risk_levels

    # Rank Vendors
    ranked_df = df.sort_values(
        by="Score",
        ascending=False
    )

    ranked_df.reset_index(
        drop=True,
        inplace=True
    )

    return ranked_df