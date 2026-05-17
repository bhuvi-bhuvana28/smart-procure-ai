import pandas as pd


def calculate_scores(df):

    max_price = df["Price"].max()
    max_delivery = df["Delivery_Days"].max()
    max_warranty = df["Warranty_Years"].max()
    max_support = df["Support_Rating"].max()

    scores = []

    for _, row in df.iterrows():

        # Lower price is better
        price_score = (
            (max_price - row["Price"]) / max_price
        ) * 40

        # Faster delivery is better
        delivery_score = (
            (max_delivery - row["Delivery_Days"]) / max_delivery
        ) * 25

        # Higher warranty is better
        warranty_score = (
            row["Warranty_Years"] / max_warranty
        ) * 20
        # Better support is better
        support_score = (
            row["Support_Rating"] / max_support
        ) * 15

        total_score = (
            price_score +
            delivery_score +
            warranty_score +
            support_score
        )

        scores.append(round(total_score, 2))

    df["Score"] = scores

    return df.sort_values(
        by="Score",
        ascending=False
    )