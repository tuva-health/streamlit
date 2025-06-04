import sys
from pathlib import Path
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from snowflake_data import (
    get_pmpm_by_diagnosis,
    get_pmpm_by_diagnosis_category,
)

# Add the repo root (analytics/) to sys.path so we can import shared modules
sys.path.append(str(Path(__file__).resolve().parents[3]))

from shared import path_utils
path_utils.add_repo_to_path(levels_up=3)

conn = st.connection("snowflake")
year = st.session_state.get("page_selector") if "page_selector" in st.session_state else None

pmpm_diagnosis_category = get_pmpm_by_diagnosis_category(conn, year)
pmpm_diagnosis = get_pmpm_by_diagnosis(conn, year)

def truncate_label(label, max_length=30):
    return str(label) if len(str(label)) <= max_length else str(label)[:max_length] + "..."

truncated_category_labels = [truncate_label(label, 40) for label in pmpm_diagnosis_category["DX_CCSR_CATEGORY2"]]
full_category_labels = pmpm_diagnosis_category["DX_CCSR_CATEGORY2"].tolist()

truncated_labels = [truncate_label(label, 40) for label in pmpm_diagnosis["DX_DESCRIPTION"]]
full_labels = pmpm_diagnosis["DX_DESCRIPTION"].tolist()

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
        x=pmpm_diagnosis_category["PERCENT_OF_TOTAL_PMPM"],
        y=pmpm_diagnosis_category["DX_CCSR_CATEGORY2"],
        text=[f"{x:.1f} %" for x in pmpm_diagnosis_category["PERCENT_OF_TOTAL_PMPM"]],
        textposition='outside',
        cliponaxis=False,
        orientation='h',
        showlegend=False,
        customdata=pmpm_diagnosis_category["DX_CCSR_CATEGORY2"],
        hovertemplate="<b>%{customdata}</b><br>PMPM: %{x:.1f}%<extra></extra>",
    ),
    row=1, col=1
)

# Bar 2: Cumulative Paid PMPM
diagnosis_category_fig.add_trace(
    go.Bar(
        x=pmpm_diagnosis_category["CUMULATIVE_PMPM"],
        y=pmpm_diagnosis_category["DX_CCSR_CATEGORY2"],
        text=[f"${int(round(x)):,}" for x in pmpm_diagnosis_category["CUMULATIVE_PMPM"]],
        textposition='outside',
        cliponaxis=False,
        orientation='h',
        showlegend=False,
        customdata=pmpm_diagnosis_category["DX_CCSR_CATEGORY2"],
        hovertemplate="<b>%{customdata}</b><br>Cumulative PMPM: $%{x:,.0f}<extra></extra>",
    ),
    row=1, col=2
)

category_count = len(full_category_labels)
category_height = min(max(60 * category_count, 400), 3000)

diagnosis_category_fig.update_xaxes(showticklabels=False)

diagnosis_category_fig.update_layout(
    height=category_height,
    width=1200,
    margin=dict(l=150, b=10, t=45, r=55),
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
        x=pmpm_diagnosis["PERCENT_OF_TOTAL_PMPM"],
        y=pmpm_diagnosis["DX_DESCRIPTION"],
        text=[f"{x:.1f}" for x in pmpm_diagnosis["PERCENT_OF_TOTAL_PMPM"]],
        textposition='outside',
        cliponaxis=False,
        orientation='h',
        showlegend=False,
        customdata=pmpm_diagnosis["DX_DESCRIPTION"],
        hovertemplate="<b>%{customdata}</b><br>PMPM: %{x:.1f}%<extra></extra>",
    ),
    row=1, col=1
)

# Bar 2: Cumulative Paid PMPM
diagnosis_fig.add_trace(
    go.Bar(
        x=pmpm_diagnosis["CUMULATIVE_PMPM"],
        y=pmpm_diagnosis["DX_DESCRIPTION"],
        text=[f"${int(round(x)):,}" for x in pmpm_diagnosis["CUMULATIVE_PMPM"]],
        textposition='outside',
        cliponaxis=False,
        orientation='h',
        showlegend=False,
        customdata=pmpm_diagnosis["DX_DESCRIPTION"],
        hovertemplate="<b>%{customdata}</b><br>Cumulative PMPM: $%{x:,.0f}<extra></extra>",
    ),
    row=1, col=2
)

diagnosis_count = len(full_labels)
diagnosis_height = min(max(60 * diagnosis_count, 400), 3000)

diagnosis_fig.update_xaxes(showticklabels=False)

diagnosis_fig.update_layout(
    height=diagnosis_height,
    width=1200,
    margin=dict(l=150, b=10, t=45, r=55),
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

st.markdown("<h5 style='text-align: center; font-weight: bold; padding-bottom: 0;'>Diagnosis</h3>", unsafe_allow_html=True)
st.plotly_chart(diagnosis_fig, use_container_width=True, key="diagnosis-chart")
