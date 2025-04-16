import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from utils.helpers import get_table_data

conn = st.connection("snowflake")

"""
# Claim Amount Analysis

This page allows you to analyze the amount spent for each claim line number. You can filter the data based on the amount paid and select a category to analyze.
## Instructions
1. Use the dropdown to select a category to analyze.
2. The rose chart and histogram will display the distribution of the amount spent for each claim line by the selected category.
3. The table will display the filtered data with the selected category and amount paid.
"""

data = get_table_data(conn)

# Dropdown to select where the expense was made.
spent_category_options = {
    "Encounter Group": "ENCOUNTER_GROUP",
    "Encounter Type": "ENCOUNTER_TYPE",
    "Service Category 1": "SERVICE_CATEGORY_1",
    "Service Category 2": "SERVICE_CATEGORY_2",
    "Service Category 3": "SERVICE_CATEGORY_3",
}
col1, col2 = st.columns([3, 1])
with col1:
    selected_category_label = st.selectbox(
        "Select Category to Analyze",
        options=list(spent_category_options.keys()),
        index=0,
    )
selected_category = spent_category_options[selected_category_label]

# Paid amount range slider.
max_range = data["PAID_AMOUNT"].max()

agg_data = data.groupby(selected_category, as_index=False)["PAID_AMOUNT"].sum()
rose_fig = px.bar_polar(
    agg_data,
    r="PAID_AMOUNT",
    labels={"PAID_AMOUNT": "Total Amount Paid"},
    theta=selected_category,
    title=f"Distribution of Amount spent for each Claim Line by {selected_category_label}",
    color=selected_category
)

rose_fig

# Display the histogram.
fig = px.histogram(
    data,
    x=selected_category,
    y="PAID_AMOUNT",
    histfunc="sum",
    title=f"Distribution of Amount spent for each Claim Line by {selected_category_label}",
    labels={"PAID_AMOUNT": "Amount Paid"},
)
fig

# Display the line chart.

"""
## Expense Detail
"""

data["CLAIM_START_DATE"] = pd.to_datetime(data["CLAIM_START_DATE"].astype(str), errors="coerce").dt.strftime("%Y-%m")

# Sum total paid and total allowed amounts by month
monthly_agg = (
    data.groupby("CLAIM_START_DATE")[["PAID_AMOUNT", "ALLOWED_AMOUNT"]]
    .sum()
    .reset_index()
)


#  using plotly line chart.
fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=monthly_agg["CLAIM_START_DATE"],
        y=monthly_agg["PAID_AMOUNT"],
        mode="lines+markers",
        name="Total Paid",
    )
)

fig.add_trace(
    go.Scatter(
        x=monthly_agg["CLAIM_START_DATE"],
        y=monthly_agg["ALLOWED_AMOUNT"],
        mode="lines+markers",
        name="Total Allowed",
    )
)

fig.update_layout(
    title="Monthly Total Paid and Allowed Amounts",
    xaxis_title="Date",
    yaxis_title="Amount",
    legend_title="Metric",
    hovermode="x unified",
    template="plotly_white",
)

# Add range slider
fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list(
            [
                dict(count=1, label="1M", step="month", stepmode="backward"),
                dict(count=3, label="3M", step="month", stepmode="backward"),
                dict(count=6, label="6M", step="month", stepmode="backward"),
                dict(step="all"),
            ]
        )
    ),
)

# Display in streamlit
st.plotly_chart(fig, use_container_width=True)