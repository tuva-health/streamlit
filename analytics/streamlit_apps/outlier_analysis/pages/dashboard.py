import sys
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components
import plotly.express as px
import pandas as pd

sys.path.append(str(Path(__file__).resolve().parents[3]))
from shared.utils.outlier_helpers import (
    get_outlier_population_by_race,
    get_outlier_population_by_state,
)
from shared import path_utils

# Add the repo root (analytics/) to sys.path so we can import shared modules
path_utils.add_repo_to_path(levels_up=3)

conn = st.connection("snowflake")
population_by_state = pd.DataFrame(get_outlier_population_by_state(conn, year=2018))
population_by_race = pd.DataFrame(get_outlier_population_by_race(conn, year=2018))
# population_by_race['PERCENTAGE_LABEL'] = population_by_race['PERCENTAGE'].astype(str) + '%'

# --- Page Title and Description ---
st.header("Medicare LDS Outlier Cost Driver Dashboard", divider="grey")
st.markdown(
    "This dashboard presents key metrics and visualizations for outlier cost drivers in the 2020 Medicare LDS 5% Sample."
)

st.write("####")  # Add blank space between sections

with st.container():
    col1, col2, col3 = st.columns([1, 1, 1], gap="large")
    with col1:
        html = """
                <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                    <div style="display: flex; justify-content: space-between; font-size: 1.2rem;">
                        <span style="font-weight: bold;">Members</span>
                        <span>61,674</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 1.2rem;">
                        <span style="font-weight: bold;">Mean Age</span>
                        <span>77</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 1.2rem;">
                        <span style="font-weight: bold;">Percent Female</span>
                        <span>50.4%</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 1.2rem;">
                        <span style="font-weight: bold;">Average HCC Risk Score</span>
                        <span>4.14</span>
                    </div>
                """
        st.markdown(html, unsafe_allow_html=True)

    with col2:
        html = """
            <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                <div style="display: flex; justify-content: space-between; font-size: 1.2rem;">
                    <span style="font-weight: bold;">Paid Amount</span>
                    <span>$6.6B</span>
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 1.2rem;">
                    <span style="font-weight: bold;">Paid PMPM</span>
                    <span>$9,776</span>
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 1.2rem;">
                    <span style="font-weight: bold;">Encounter Per 1000</span>
                    <span>91,671</span>
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 1.2rem;">
                    <span style="font-weight: bold;">Paid Per Encounter</span>
                    <span>1,280</span>
                </div>
            """
        st.markdown(html, unsafe_allow_html=True)

    with col3:
        html = """
        <div style="font-size: 1.2rem;"><span style="font-weight:bold"> Data Source </span> : 2020 Medicare LDS 5% Sample </div>
        <div style="font-size: 1.2rem;"><span style="font-weight:bold">Inclusion Criteria</span>: All beneficiaries with annual claim costs > 2 std dev from mean ($61,857)
        """
        st.markdown(html, unsafe_allow_html=True)


st.write("####")  # Add blank space between sections

with st.container():
    graph1, graph2 = st.columns([1, 1], gap="large")
    with graph1:
        st.subheader("Outlier Population by State")
        fig = px.bar(
            population_by_state,
            x="PERCENTAGE",
            y="STATE",
            orientation="h",
            text="PERCENTAGE",
            height=1000,
        )
        fig.update_layout(
            showlegend=False, 
            margin=dict(r=80),
            yaxis_title="",
            yaxis=dict(automargin=True),
        )
        fig.update_traces(
            marker_color="#66B1E2",
            textposition="outside",
            textfont=dict(size=12),
            cliponaxis=False,
        )
        # Embed Plotly chart in a scrollable div using components.html
        plot_html = fig.to_html(full_html=False, include_plotlyjs="cdn")
        components.html(
            f"""
            <div style="overflow-y: auto; height: 500px;">
                {plot_html}
            </div>
            """,
            height=520,  # Slightly more than 500px to account for padding/borders
            scrolling=True,
        )

    with graph2:
        st.subheader("Outlier Population by Race")
        fig = px.bar(
            population_by_race,
            x="PERCENTAGE",
            y="RACE",
            orientation="h",
            text="PERCENTAGE",
            height=300,
        )
        fig.update_layout(showlegend=False, margin=dict(r=80))

        fig.update_traces(
            marker_color="#66B1E2",
            textposition="outside",
            textfont=dict(size=12),
            cliponaxis=False,
        )
        st.plotly_chart(fig, use_container_width=True)
