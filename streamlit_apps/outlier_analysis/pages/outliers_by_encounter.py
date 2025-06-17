import plotly.graph_objects as go
import streamlit as st
from csv_data import (
    get_pmpm_and_encounters_by_group_csv,
    get_pmpm_and_encounters_by_type_csv,
)
from plotly.subplots import make_subplots

year = st.session_state.get("selected_year") if "selected_year" in st.session_state else None

outlier_encounter_group_data = get_pmpm_and_encounters_by_group_csv(year)
outlier_encouter_type_data = get_pmpm_and_encounters_by_type_csv(year)

encounter_groups = outlier_encounter_group_data["ENCOUNTER_GROUP"].unique()

color_map = {
    "null": "#D3D3D3",
    "inpatient": "#0A3F5C",
    "office based": "#FDCB0A",
    "other": "#0FB594",
    "outpatient": "#64B0E1",
    "Grand Total": "#5C6068"
}

def get_colors_for_df(df):
    return [color_map[etype] for etype in df['ENCOUNTER_GROUP']]

encounter_group_fig = make_subplots(
    rows=1, cols=3,
    shared_yaxes=True,
    horizontal_spacing=0.1,
    subplot_titles=("Paid PMPM", "Encounters per 1000", "Paid Per Encounter")
)

# Bar 1: PMPM
encounter_group_fig.add_trace(
    go.Bar(
        x=outlier_encounter_group_data["PMPM"],
        y=outlier_encounter_group_data["ENCOUNTER_GROUP"],
        marker_color=get_colors_for_df(outlier_encounter_group_data),
        text=[f"${int(round(x)):,}" for x in outlier_encounter_group_data["PMPM"]],
        textposition='outside',
        cliponaxis=False,
        orientation='h',
        showlegend=False,
        hovertemplate=(
            "<b>Encounter Group:</b> %{customdata[0]}<br>" +
            "<b>Paid PMPM:</b> $%{x:,.0f}<extra></extra>"
        ),
        customdata=outlier_encounter_group_data[["ENCOUNTER_GROUP"]].values
    ),
    row=1, col=1
)

# Bar 2: Encounters per 1000
encounter_group_fig.add_trace(
    go.Bar(
        x=outlier_encounter_group_data["ENCOUNTERS_PER_1000"],
        y=outlier_encounter_group_data["ENCOUNTER_GROUP"],
        marker_color=get_colors_for_df(outlier_encounter_group_data),
        text=[f"{int(round(x)):,}" for x in outlier_encounter_group_data["ENCOUNTERS_PER_1000"]],
        textposition='outside',
        cliponaxis=False,
        orientation='h',
        showlegend=False,
        hovertemplate=(
            "<b>Encounter Group:</b> %{customdata[0]}<br>" +
            "<b>Encounters Per 1000:</b> %{x:,.0f}<extra></extra>"
        ),
        customdata=outlier_encounter_group_data[["ENCOUNTER_GROUP"]].values
    ),
    row=1, col=2
)

# Bar 3: Paid per Encounter
encounter_group_fig.add_trace(
    go.Bar(
        x=outlier_encounter_group_data["PAID_PER_ENCOUNTER"],
        y=outlier_encounter_group_data["ENCOUNTER_GROUP"],
        marker_color=get_colors_for_df(outlier_encounter_group_data),
        text=[f"${int(round(x)):,}" for x in outlier_encounter_group_data["PAID_PER_ENCOUNTER"]],
        textposition='outside',
        cliponaxis=False,
        orientation='h',
        showlegend=False,
        hovertemplate=(
            "<b>Encounter Group:</b> %{customdata[0]}<br>" +
            "<b>Paid Per Encounter:</b> $%{x:,.0f}<extra></extra>"
        ),
        customdata=outlier_encounter_group_data[["ENCOUNTER_GROUP"]].values
    ),
    row=1, col=3
)

encounter_group_fig.update_xaxes(showticklabels=False)

encounter_group_fig.update_layout(
    height=220,
    width=1200,
    margin=dict(l=150, b=10, r=65),
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
    horizontal_spacing=0.1,
    subplot_titles=("Paid PMPM", "Encounters per 1000", "Paid Per Encounter")
)

# Bar 1: PMPM
encounter_type_fig.add_trace(
    go.Bar(
        x=outlier_encouter_type_data["PMPM"],
        y=outlier_encouter_type_data["ENCOUNTER_TYPE"],
        marker_color=get_colors_for_df(outlier_encouter_type_data),
        text=[f"${int(round(x)):,}" for x in outlier_encouter_type_data["PMPM"]],
        textposition='outside',
        cliponaxis=False,
        orientation='h',
        showlegend=False,
        hovertemplate=(
            "<b>Encounter Group:</b> %{customdata[0]}<br>" +
            "<b>Encounter Type:</b> %{y}<br>" +
            "<b>Paid PMPM:</b> $%{x:,.0f}<extra></extra>"
        ),
        customdata=outlier_encouter_type_data[["ENCOUNTER_GROUP"]].values
    ),
    row=1, col=1
)

# Bar 2: Encounters per 1000
encounter_type_fig.add_trace(
    go.Bar(
        x=outlier_encouter_type_data["ENCOUNTERS_PER_1000"],
        y=outlier_encouter_type_data["ENCOUNTER_TYPE"],
        marker_color=get_colors_for_df(outlier_encouter_type_data),
        text=[f"{int(round(x)):,}" for x in outlier_encouter_type_data["ENCOUNTERS_PER_1000"]],
        textposition='outside',
        cliponaxis=False,
        orientation='h',
        showlegend=False,
        hovertemplate=(
            "<b>Encounter Group:</b> %{customdata[0]}<br>" +
            "<b>Encounter Type:</b> %{y}<br>" +
            "<b>Encounters Per 1000:</b> %{x:,.0f}<extra></extra>"
        ),
        customdata=outlier_encouter_type_data[["ENCOUNTER_GROUP"]].values
    ),
    row=1, col=2
)

# Bar 3: Paid per Encounter
encounter_type_fig.add_trace(
    go.Bar(
        x=outlier_encouter_type_data["PAID_PER_ENCOUNTER"],
        y=outlier_encouter_type_data["ENCOUNTER_TYPE"],
        marker_color=get_colors_for_df(outlier_encouter_type_data),
         text=[f"${int(round(x)):,}" for x in outlier_encouter_type_data["PAID_PER_ENCOUNTER"]],
        textposition='outside',
        cliponaxis=False,
        orientation='h',
        showlegend=False,
        hovertemplate=(
            "<b>Encounter Group:</b> %{customdata[0]}<br>" +
            "<b>Encounter Type:</b> %{y}<br>" +
            "<b>Paid Per Encounter:</b> $%{x:,.0f}<extra></extra>"
        ),
        customdata=outlier_encouter_type_data[["ENCOUNTER_GROUP"]].values
    ),
    row=1, col=3
)

encounter_type_fig.update_xaxes(showticklabels=False)

encounter_type_fig.update_layout(
    height=500,
    width=1200,
    title=dict(
        text="Encounter Type",
        x=0.5,
        xanchor='center',
        font=dict(size=20)
    ),
    margin=dict(b=2, r=65),
)

st.plotly_chart(encounter_type_fig, use_container_width=True)

st.markdown("""
    <style>
        #fixed-legend-container {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            width: 100%;
            background-color: white;
            border-top: 1px solid #ddd;
            padding: 10px 20px;
            z-index: 10;
        }

        .legend-row {
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
            justify-content: center;
        }

        .legend-item {
            display: flex;
            align-items: center;
        }

        .legend-color {
            width: 16px;
            height: 16px;
            margin-right: 8px;
            border: 1px solid #ccc;
        }
    </style>
""", unsafe_allow_html=True)


# Legend HTML block
legend_html = "<div id='fixed-legend-container'><div class='legend-row'>"

for encounter_group, color in color_map.items():
    legend_html += (
        f"<div class='legend-item'>"
        f"<div class='legend-color' style='background-color: {color};'></div>"
        f"<span>{encounter_group}</span>"
        f"</div>"
    )

legend_html += "</div></div>"

st.markdown(legend_html, unsafe_allow_html=True)