import sys
from pathlib import Path
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

sys.path.append(str(Path(__file__).resolve().parents[3]))
from data import (
    get_metrics_data,
    get_mean_paid,
    get_outlier_population_by_race,
    get_outlier_population_by_state,
    get_v24_risk_scores
)
from shared import path_utils

# Add the repo root (analytics/) to sys.path so we can import shared modules
path_utils.add_repo_to_path(levels_up=3)


def safe_extract(series, default=0, as_type=float):
    """Safely extract first item from a Series and convert to given type."""
    if isinstance(series, pd.Series) and not series.empty and pd.notna(series.iloc[0]):
        return as_type(series.iloc[0])
    return default


def display_metrics(metrics_data, year):
    """Display summary metrics in columns."""

    # Extract and sanitize values
    total_population = safe_extract(metrics_data.get("MEMBER_MONTHS"), default=0, as_type=int)
    female_count = safe_extract(metrics_data.get("FEMALE_COUNT"), default=0, as_type=float)
    mean_age = safe_extract(metrics_data.get("MEAN_AGE"), default="N/A", as_type=float)
    total_paid = safe_extract(metrics_data.get("TOTAL_PAID"), default=0.0, as_type=float)
    total_encounters = safe_extract(metrics_data.get("TOTAL_ENCOUNTERS"), default=0, as_type=int)
    mean_paid = safe_extract(metrics_data.get("MEAN_PAID"), default=0.0, as_type=float)

    # Compute derived metrics safely
    percent_female = (female_count / total_population) * 100 if total_population else 0.0
    encounter_per_1000 = (total_encounters / total_population) * 12000 if total_population else 0.0
    paid_per_encounter = (total_paid / total_encounters) if total_encounters else 0.0
    paid_pmpm = (total_paid / total_population) if total_population else 0.0

    col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 4], gap="small")
    with col1:
        st.metric(label="Members", value=total_population, border=True)
        st.metric("Mean Age **(Yrs)**", f"{mean_age:,.2f}", border=True)

    with col2:
        st.metric("Percent Female **(%)**", f"{percent_female:.2f}", border=True)
        st.metric("Avg HCC Risk Score", "4.14", border=True)  # Replace with actual value if available

    with col3:
        st.metric("Paid Amount **($)**", total_paid, border=True)
        st.metric("Paid PMPM **($)**", f"{paid_pmpm:,.2f}", border=True)

    with col4:
        st.metric("Encounter / 1000", f"{encounter_per_1000:.2f}", border=True)
        st.metric("Paid / Encounter **($)**", f"{paid_per_encounter:,.2f}", border=True)

    with col5:
        st.markdown(
            f"""
            **Inclusion Criteria:** All beneficiaries with annual claim costs > 2 std dev from mean (${mean_paid:.2f})
            """
        )

        st.markdown(
        """
            <style>
            [data-testid="stMetricValue"] {
                font-size: 14px;
                font-weight: 700;
            }
            </style>
        """,
            unsafe_allow_html=True,
        )
def plot_bar_chart(df, x, y, title, height=260):
        """Create a horizontal bar chart with Plotly."""
        fig = px.bar(
            df,
            x=x,
            y=y,
            orientation="h",
            text=x,
            height=height,
            color=y
        )
        fig.update_layout(
            showlegend=False,
            margin=dict(r=80),
            xaxis_title=x,
            yaxis_title=y,
            yaxis=dict(
                automargin=True,
            ),
            title=title,
        )
        fig.update_traces(
            marker_color= None if y == "RACE" else '#66B1E2',
            textposition="outside",
            texttemplate="%{text}%" if x == "PERCENTAGE" else "%{text}",
            cliponaxis=False,
        )
        return fig

def plot_risk_scores(risk_scores):
    """Plot risk scores distribution."""
    # Calculate min, median, and max
    min_val = risk_scores["RISK_SCORE"].min()
    median_val = risk_scores["RISK_SCORE"].median()
    max_val = risk_scores["RISK_SCORE"].max()

    # Create a custom box plot showing only min, median, and max
    fig = go.Figure()
    fig.add_trace(go.Box(
        y=[min_val, median_val, max_val],
        boxpoints=False,
        name="Risk Score",
        marker_color="#66B1E2",
        boxmean=True,
        showlegend=False
    ))
    fig.update_layout(
        title="Risk Score Distribution (Min, Median, Max)",
        yaxis_title="V24 Risk Score",
        xaxis_title="",
        height=320
    )

    return fig

def main():
    st.markdown(
        """
        <style>
            .stMainBlockContainer  {
                padding-left: 1rem;
                padding-right: 1rem;
                padding-top: 3rem;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
    year = st.session_state.get("page_selector") if "page_selector" in st.session_state else None
    conn = st.connection("snowflake")
    mean_paid = get_mean_paid(conn, year).iloc[0]
    metrics_data = get_metrics_data(conn, year)
    metrics_data["MEAN_PAID"] = mean_paid
    outlier_population_by_state = get_outlier_population_by_state(conn, year)
    outlier_population_by_race = get_outlier_population_by_race(conn, year)
    v24_risk_scores = get_v24_risk_scores(conn, year)

    # --- Page Title and Description ---
    st.header("Outlier Cost Driver Dashboard", divider="grey")
    st.markdown(
        f"This dashboard presents key metrics and visualizations for outlier cost drivers in the year {year}"
    )

    display_metrics(metrics_data, year)

    with st.container():
        graph1, graph2 = st.columns([1, 1], gap="large")
        with graph1:
            with st.container():
                fig = plot_bar_chart(outlier_population_by_state, "PERCENTAGE", "STATE", "Outlier Population by State", 650)
                st.plotly_chart(fig, use_container_width=True)
        with graph2:
            fig = plot_bar_chart(outlier_population_by_race, "PERCENTAGE", "RACE", "Outlier Population by Race")
            st.plotly_chart(fig, use_container_width=True)

            risk_score_fig = plot_risk_scores(v24_risk_scores)
            st.plotly_chart(risk_score_fig, use_container_width=True)

if __name__ == "__main__":
    main()