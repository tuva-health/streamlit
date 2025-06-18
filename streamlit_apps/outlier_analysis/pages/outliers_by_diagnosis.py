import sys
from pathlib import Path
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from csv_data import (
    get_pmpm_by_diagnosis_category_csv,
    get_pmpm_by_diagnosis_csv
)



# Add the repo root (analytics/) to sys.path so we can import shared modules
sys.path.append(str(Path(__file__).resolve().parents[3]))

from shared import path_utils
path_utils.add_repo_to_path(levels_up=3)

year = st.session_state.get("selected_year") if "selected_year" in st.session_state else None

# Add slider to select the number of diagnoses to show
top_n = st.sidebar.slider("Number of Diagnoses to Show", 10, 500, 100, step=1) 


# Use of local CSV files instead of Snowflake queries

diagnosis_category_data = get_pmpm_by_diagnosis_category_csv(year)
diagnosis_category_data = diagnosis_category_data.sort_values(by="PERCENT_OF_TOTAL_PMPM", ascending=False).head(top_n)

diagnosis_data = get_pmpm_by_diagnosis_csv(year)
diagnosis_data = diagnosis_data.sort_values(by="PERCENT_OF_TOTAL_PMPM", ascending=False).head(top_n)


# diagnosis_category_data = get_pmpm_by_diagnosis_category_csv(year)
# diagnosis_data = get_pmpm_by_diagnosis_csv(year)

def truncate_label(label, max_length=30):
    return str(label) if len(str(label)) <= max_length else str(label)[:max_length] + "..."

truncated_category_labels = [truncate_label(label, 40) for label in diagnosis_category_data["DX_CCSR_CATEGORY2"]]
full_category_labels = diagnosis_category_data["DX_CCSR_CATEGORY2"].tolist()

truncated_labels = [truncate_label(label, 40) for label in diagnosis_data["DX_DESCRIPTION"]]
full_labels = diagnosis_data["DX_DESCRIPTION"].tolist()

st.markdown(
    """
    <style>
        .st-key-diagnosis-category-chart {
            height: 300px;
            overflow: scroll;
        }
        .st-key-diagnosis-chart {
            height: 300px;
            overflow: scroll;
        }
    </style>
    """,
    unsafe_allow_html=True
)

diagnosis_category_fig = make_subplots(
    rows=1, cols=2,
    column_widths=[0.5, 0.5],
    shared_yaxes=True,
    horizontal_spacing=0.05,
    subplot_titles=("% of Paid PMPM", "Cumulative Paid PMPM")
)

# Bar 1: % of Paid PMPM
diagnosis_category_fig.add_trace(
    go.Bar(
        x=diagnosis_category_data["PERCENT_OF_TOTAL_PMPM"],
        y=diagnosis_category_data["DX_CCSR_CATEGORY2"],
        text=[f"{x:.1f} %" for x in diagnosis_category_data["PERCENT_OF_TOTAL_PMPM"]],
        textposition='outside',
        cliponaxis=False,
        orientation='h',
        showlegend=False,
        customdata=diagnosis_category_data["DX_CCSR_CATEGORY2"],
        hovertemplate="<b>%{customdata}</b><br>PMPM: %{x:.1f}%<extra></extra>",
    ),
    row=1, col=1
)

# Bar 2: Cumulative Paid PMPM
diagnosis_category_fig.add_trace(
    go.Bar(
        x=diagnosis_category_data["CUMULATIVE_PMPM"],
        y=diagnosis_category_data["DX_CCSR_CATEGORY2"],
        text=[f"${int(round(x)):,}" for x in diagnosis_category_data["CUMULATIVE_PMPM"]],
        textposition='outside',
        cliponaxis=False,
        orientation='h',
        showlegend=False,
        customdata=diagnosis_category_data["DX_CCSR_CATEGORY2"],
        hovertemplate="<b>%{customdata}</b><br>Cumulative PMPM: $%{x:,.0f}<extra></extra>",
    ),
    row=1, col=2
)

category_count = len(full_category_labels)
category_height = min(max(60 * category_count, 400), 2000)

diagnosis_category_fig.update_layout(
    height=category_height,
    width=1200,
    margin=dict(l=150, b=10, t=45, r=55),
    xaxis=dict(
        showticklabels=False,
    ),
    yaxis=dict(
        tickmode="array",
        tickvals=full_category_labels,
        ticktext=truncated_category_labels,
        tickfont=dict(size=11)
    ),
    yaxis2=dict(
        tickmode="array",
        tickvals=full_category_labels,
        ticktext=truncated_category_labels,
        tickfont=dict(size=11)
    ),
    hovermode='y',
)

#make it so highest percent paid pmpm category is at the top
diagnosis_category_fig.update_yaxes(autorange="reversed")


st.markdown("<h5 style='text-align: center; font-weight: bold; padding-bottom: 0;'>Diagnosis Category</h3>", unsafe_allow_html=True)
st.plotly_chart(diagnosis_category_fig, use_container_width=True, key="diagnosis-category-chart")



diagnosis_fig = make_subplots(
    rows=1, cols=2,
    column_widths=[0.5, 0.5],
    shared_yaxes=True,
    horizontal_spacing=0.05,
    subplot_titles=("% of Paid PMPM", "Cumulative Paid PMPM")
)

# Bar 1: % of Paid PMPM
diagnosis_fig.add_trace(
    go.Bar(
        x=diagnosis_data["PERCENT_OF_TOTAL_PMPM"],
        y=diagnosis_data["DX_DESCRIPTION"],
        text=[f"{x:.1f}" for x in diagnosis_data["PERCENT_OF_TOTAL_PMPM"]],
        textposition='outside',
        cliponaxis=False,
        orientation='h',
        showlegend=False,
        customdata=diagnosis_data["DX_DESCRIPTION"],
        hovertemplate="<b>%{customdata}</b><br>PMPM: %{x:.1f}%<extra></extra>",
    ),
    row=1, col=1
)

# Bar 2: Cumulative Paid PMPM
diagnosis_fig.add_trace(
    go.Bar(
        x=diagnosis_data["CUMULATIVE_PMPM"],
        y=diagnosis_data["DX_DESCRIPTION"],
        text=[f"${int(round(x)):,}" for x in diagnosis_data["CUMULATIVE_PMPM"]],
        textposition='outside',
        cliponaxis=False,
        orientation='h',
        showlegend=False,
        customdata=diagnosis_data["DX_DESCRIPTION"],
        hovertemplate="<b>%{customdata}</b><br>Cumulative PMPM: $%{x:,.0f}<extra></extra>",
    ),
    row=1, col=2
)

diagnosis_count = len(full_labels)
diagnosis_height = min(max(60 * diagnosis_count, 400), 3000)

diagnosis_fig.update_layout(
    height=diagnosis_height,
    width=1200,
    margin=dict(l=150, b=10, t=45, r=55),
    xaxis=dict(
        showticklabels=False,
    ),
    yaxis=dict(
        tickmode="array",
        tickvals=full_labels,
        ticktext=truncated_labels,
        tickfont=dict(size=11)
    ),
    yaxis2=dict(
        tickmode="array",
        tickvals=full_labels,
        ticktext=truncated_labels,
        tickfont=dict(size=11)
    ),
    hovermode='y',
)
diagnosis_fig.update_yaxes(autorange="reversed")


st.markdown("<h5 style='text-align: center; font-weight: bold; padding-bottom: 0;'>Diagnosis</h3>", unsafe_allow_html=True)
st.plotly_chart(diagnosis_fig, use_container_width=True, key="diagnosis-chart")


