import sys
from pathlib import Path
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from data import (
    get_encounters_per_1000_by_encounter_group,
    get_encounters_per_1000_by_encounter_type,
    get_paid_per_encounter_by_encounter_group,
    get_paid_per_encounter_by_encounter_type,
    get_pmpm_by_encounter_group,
    get_pmpm_by_encounter_type
)

# Add the repo root (analytics/) to sys.path so we can import shared modules
sys.path.append(str(Path(__file__).resolve().parents[3]))

from shared import path_utils
path_utils.add_repo_to_path(levels_up=3)

conn = st.connection("snowflake")

pmpm_group = get_pmpm_by_encounter_group(conn).fillna('null')
per_1000_group = get_encounters_per_1000_by_encounter_group(conn).fillna('null')
paid_per_group = get_paid_per_encounter_by_encounter_group(conn).fillna('null')

pmpm_type = get_pmpm_by_encounter_type(conn).fillna('null')
per_1000_type = get_encounters_per_1000_by_encounter_type(conn).fillna('null')
paid_per_type = get_paid_per_encounter_by_encounter_type(conn).fillna('null')

encounter_groups = pmpm_group["ENCOUNTER_GROUP"].unique()

color_map = {etype: px.colors.qualitative.Plotly[i % 10]
                      for i, etype in enumerate(encounter_groups)}

def get_colors_for_df(df):
    return [color_map[etype] for etype in df['ENCOUNTER_GROUP']]

st.markdown(
    """
    <style>
        .stMainBlockContainer  {
            padding-left: 1rem;
            padding-right: 1rem;
            padding-top: 2rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Encounter Group Chart
encounter_group_fig = make_subplots(
    rows=1, cols=3,
    shared_yaxes=True,
    horizontal_spacing=0.05,
    subplot_titles=("Paid PMPM", "Encounters per 1000", "Paid Per Encounter")
)

# Bar 1: PMPM
encounter_group_fig.add_trace(
    go.Bar(
        x=pmpm_group["PMPM"],
        y=pmpm_group["ENCOUNTER_GROUP"],
        marker_color=get_colors_for_df(pmpm_group),
        text=[f"${x:.2f}" for x in pmpm_group["PMPM"]],
        orientation='h',
        showlegend=False,
    ),
    row=1, col=1
)

# Bar 2: Encounters per 1000
encounter_group_fig.add_trace(
    go.Bar(
        x=per_1000_group["ENCOUNTERS_PER_1000"],
        y=per_1000_group["ENCOUNTER_GROUP"],
        marker_color=get_colors_for_df(per_1000_group),
        text=[f"{x:.2f}" for x in per_1000_group["ENCOUNTERS_PER_1000"]],
        orientation='h',
        showlegend=False
    ),
    row=1, col=2
)

# Bar 3: Paid per Encounter
encounter_group_fig.add_trace(
    go.Bar(
        x=paid_per_group["PAID_PER_ENCOUNTER"],
        y=paid_per_group["ENCOUNTER_GROUP"],
        marker_color=get_colors_for_df(paid_per_group),
        text=[f"${x:.2f}" for x in paid_per_group["PAID_PER_ENCOUNTER"]],
        orientation='h',
        showlegend=False
    ),
    row=1, col=3
)

# Layout settings
encounter_group_fig.update_layout(
    height=220,
    width=1200,
    margin=dict(l=150, b=10),
    title=dict(
        text="Encounter Group",
        x=0.5,
        xanchor='center',
        font=dict(size=20)
    )
)

st.plotly_chart(encounter_group_fig, use_container_width=True)

encounter_type_fig = make_subplots(
    rows=1, cols=3,
    shared_yaxes=True,
    horizontal_spacing=0.05,
    subplot_titles=("Paid PMPM", "Encounters per 1000", "Paid Per Encounter")
)

# Bar 1: PMPM
encounter_type_fig.add_trace(
    go.Bar(
        x=pmpm_type["PMPM"],
        y=pmpm_type["ENCOUNTER_TYPE"],
        marker_color=get_colors_for_df(pmpm_type),
        text=[f"${x:.2f}" for x in pmpm_type["PMPM"]],
        orientation='h',
        showlegend=False
    ),
    row=1, col=1
)

# Bar 2: Encounters per 1000
encounter_type_fig.add_trace(
    go.Bar(
        x=per_1000_type["ENCOUNTERS_PER_1000"],
        y=per_1000_type["ENCOUNTER_TYPE"],
        marker_color=get_colors_for_df(per_1000_type),
        text=[f"{x:.2f}" for x in per_1000_type["ENCOUNTERS_PER_1000"]],
        orientation='h',
        showlegend=False
    ),
    row=1, col=2
)

# Bar 3: Paid per Encounter
encounter_type_fig.add_trace(
    go.Bar(
        x=paid_per_type["PAID_PER_ENCOUNTER"],
        y=paid_per_type["ENCOUNTER_TYPE"],
        marker_color=get_colors_for_df(paid_per_type),
        text=[f"${x:.2f}" for x in paid_per_type["PAID_PER_ENCOUNTER"]],
        orientation='h',
        showlegend=False
    ),
    row=1, col=3
)

encounter_type_fig.update_layout(
    height=350,
    width=1200,
    title=dict(
        text="Encounter Type",
        x=0.5,
        xanchor='center',
        font=dict(size=20)
    ),
    margin=dict(b=2),
)

st.plotly_chart(encounter_type_fig, use_container_width=True)

legend_cols = st.columns(len(color_map))

for i, (encounter_group, color) in enumerate(color_map.items()):
    with legend_cols[i]:
        st.markdown(
            f"<div style='display: flex; align-items: center; '>"
            f"<div style='width: 20px; height: 20px; background-color: {color}; margin-right: 8px; border: 1px solid #ccc;'></div>"
            f"<span>{encounter_group}</span>"
            f"</div>",
            unsafe_allow_html=True
        )
