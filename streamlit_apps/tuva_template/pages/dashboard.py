import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from shared import path_utils
from shared.utils import helpers

path_utils.add_repo_to_path(levels_up=3)

# Add the repo root (analytics/) to sys.path so we can import shared modules
sys.path.append(str(Path(__file__).resolve().parents[3]))


# Use helper function
data = helpers.get_table_data(st.connection("snowflake"))

# Custom Styling
st.markdown(
    """
        <style>
        .stApp {background-color: #F8F9FA;}
        .css-1aumxhk {padding: 2rem 1rem;}
        .title {text-align: center; font-size: 2rem; font-weight: bold; color: #444;}
        .dropdown-label {font-weight: bold; color: #1f77b4;}
        .data-preview {color: #555; font-style: italic;}
        </style>
    """,
    unsafe_allow_html=True,
)


# Display table data
conn = st.connection("snowflake")

data = helpers.get_table_data(conn)

df = pd.DataFrame(data)

dropdown_options = {
    "Claim ID / Encounter Type": ("ENCOUNTER_TYPE", "CLAIM_ID"),
    "Claim ID / Encounter Group": ("ENCOUNTER_GROUP", "CLAIM_ID"),
    "Claim ID / Service Category 1": ("SERVICE_CATEGORY_1", "CLAIM_ID"),
    "Claim ID / Service Category 2": ("SERVICE_CATEGORY_2", "CLAIM_ID"),
    "Person ID / Encounter Type": ("ENCOUNTER_TYPE", "PERSON_ID"),
    "Person ID / Encounter Group": ("ENCOUNTER_GROUP", "PERSON_ID"),
    "Person ID / Service Category 1": ("SERVICE_CATEGORY_1", "PERSON_ID"),
    "Person ID / Service Category 2": ("SERVICE_CATEGORY_2", "PERSON_ID"),
    "Member ID / Encounter Type": ("ENCOUNTER_TYPE", "MEMBER_ID"),
    "Member ID / Encounter Group": ("ENCOUNTER_GROUP", "MEMBER_ID"),
    "Member ID / Service Category 1": ("SERVICE_CATEGORY_1", "MEMBER_ID"),
    "Member ID / Service Category 2": ("SERVICE_CATEGORY_2", "MEMBER_ID"),
}

"""
# Claim Analysis

This demo app provides an interactive visual analysis of healthcare claims data. 
Users can explore claims across different categories, such as **Encounter Type, Service Category, and Member Group**, 
to gain insights into claim distribution and trends. The app allows easy selection of dimensions for **bar charts** and **pie charts**, 
helping to identify patterns and make data-driven decisions effectively.
"""

"""
## Graphical Representation
"""
# Dropdown for X and Y axis selection
col1, col2 = st.columns([3, 1])
with col1:
    selected_label = st.selectbox(
        "Select data type", list(dropdown_options.keys()), index=0
    )
x_axis, y_axis = dropdown_options[selected_label]
st.session_state.selected_label = dropdown_options[selected_label]
color = 'ENCOUNTER_TYPE' if x_axis == 'ENCOUNTER_GROUP' else x_axis

# Pie chart data initialization.
df_count = data[x_axis].value_counts().reset_index()
df_count.columns = [x_axis, "count"]
highest = df_count["count"].max()
highest_name = df_count.loc[df_count["count"] == highest, x_axis].values[0]

a, b = st.columns(2)
a.metric(f"Highest {x_axis}", highest_name, border=True)
b.metric(f"{y_axis} Count", highest, border=True)

#  Tabs for Visualizations
tab1, tab2 = st.tabs(["📊 Bar Chart", "📈 Pie Chart"])

#  Bar Chart
tab1.subheader("📊 Bar Chart")
fig = px.histogram(
    data,
    x=x_axis,
    y=y_axis,
    histfunc="count",
    labels={x_axis: x_axis, y_axis: f"Total {y_axis}"},
    title=f"Bar Chart of {y_axis} by {x_axis}",
    color=color,
)
tab1.plotly_chart(fig, use_container_width=True)

# Pie Chart
tab2.subheader("📈 Pie Chart")

fig_pie = px.pie(
    df_count,
    names=x_axis,
    values="count",
    title=f"Pie Chart of {y_axis} by {x_axis}",
    color=x_axis,
    color_discrete_sequence=px.colors.qualitative.Set2,
)
tab2.plotly_chart(fig_pie, use_container_width=True)

"---"
"""
## Data table

Medical claims in health insurance claims data are either one of two types: institutional or professional.  Institutional claims are billed on a UB-04 claim form by facilities (e.g. hospitals) whereas professional claims are billed on a CMS-1500 claim form by physicians (e.g. your primary care doctor) and for medical supplies (e.g. durable medical equipment).  You can find a detailed overview of claim types and forms here.

In most claims datasets you'll see professional claims account for ~80% of total medical claim volume and institutional claims making up the remaining share.  The table below shows this is approximately true in the LDS dataset, however, in the synthetic dataset this proportion is flipped.  
"""
# 📄 Data Preview (Optional)
with st.expander("📄 View Data Table"):
    st.markdown(
        "<p class='data-preview'>Here’s a preview of the dataset:</p>",
        unsafe_allow_html=True,
    )
    st.dataframe(
        data,
        hide_index=True,
        column_config={data.columns[0]: {"pinned": True}},
        use_container_width=True,
    )
