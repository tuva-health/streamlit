import sys
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components
import plotly.express as px
import math
import pandas as pd

sys.path.append(str(Path(__file__).resolve().parents[3]))
from shared.utils.outlier_helpers import (
    get_metrics_data,
    get_mean_paid,
    get_outlier_population_by_race,
    get_outlier_population_by_state,
)
from shared import path_utils

# Add the repo root (analytics/) to sys.path so we can import shared modules
path_utils.add_repo_to_path(levels_up=3)


def safe_extract(series, default=0, as_type=float):
    """Safely extract first item from a Series and convert to given type."""
    if isinstance(series, pd.Series) and not series.empty and pd.notna(series.iloc[0]):
        return as_type(series.iloc[0])
    return default


def display_metrics(metrics_data):
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
        st.metric("Members", total_population, border=True)
        st.metric("Mean Age", f"{mean_age:,.2f}", border=True)

    with col2:
        st.metric("Percent Female", f"{percent_female:.2f}%", border=True)
        st.metric("Avg HCC Risk Score", "4.14", border=True)  # Replace with actual value if available

    with col3:
        st.metric("Paid Amount", f"${total_paid:,.2f}", border=True)
        st.metric("Paid PMPM", f"${paid_pmpm:,.2f}", border=True)

    with col4:
        st.metric("Encounter Per 1000", f"{encounter_per_1000:.2f}", border=True)
        st.metric("Paid Per Encounter", f"${paid_per_encounter:,.2f}", border=True)

    with col5:
        st.markdown(
            f"""
            **Data Source:** 2020 Medicare LDS 5% Sample  
            **Inclusion Criteria:** All beneficiaries with annual claim costs > 2 std dev from mean (${mean_paid:.2f})
            """
        )

        st.markdown(
        """
        <style>
        [data-testid="stMetricValue"] {
            font-size: 13px;
        }
        </style>
        """,
            unsafe_allow_html=True,
        )
def plot_bar_chart(df, x, y, title, height=300):
        """Create a horizontal bar chart with Plotly."""
        fig = px.bar(
            df,
            x=x,
            y=y,
            orientation="h",
            text=x,
            height=height,
        )
        fig.update_layout(
            font=dict(size=12, family="verdana", color="#999EA3"),
            showlegend=False,
            margin=dict(r=80),
            xaxis_title="",
            yaxis_title="",
            yaxis=dict(automargin=True),
            title=title,
        )
        fig.update_traces(
            marker_color="#66B1E2",
            textposition="outside",
            textfont=dict(size=12),
            cliponaxis=False,
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
    conn = st.connection("snowflake")
    mean_paid = get_mean_paid(conn, year="2016").iloc[0]
    metrics_data = get_metrics_data(conn, year="2016")
    metrics_data["MEAN_PAID"] = mean_paid
    outlier_population_by_state = get_outlier_population_by_state(conn, year="2017")
    outlier_population_by_race = get_outlier_population_by_race(conn, year="2017")

    # --- Page Title and Description ---
    st.header("Medicare LDS Outlier Cost Driver Dashboard", divider="grey")
    st.markdown(
        "This dashboard presents key metrics and visualizations for outlier cost drivers in the 2020 Medicare LDS 5% Sample."
    )

    display_metrics(metrics_data)

    with st.container():
        graph1, graph2 = st.columns([1, 1], gap="large")
        with graph1:
            st.subheader("Outlier Population by State")
            with st.container():
                st.markdown(
                    "<div style='padding-left:65px; font-size:1.2rem;'><b>State</b></div>",
                    unsafe_allow_html=True,
                )
                fig = plot_bar_chart(outlier_population_by_state, "PERCENTAGE", "STATE", "", 800)
                plot_html = fig.to_html(full_html=False, include_plotlyjs="cdn")
                components.html(
                    plot_html,
                    height=400,
                    scrolling=True,
                )
                st.markdown(
                    "<div style='text-align:center; font-size:1.2rem;'><b>Percentage</b></div>",
                    unsafe_allow_html=True,
                )
        with graph2:
            st.subheader("Outlier Population by Race")
            st.markdown(
                "<div style='padding-left:65px; font-size:1.2rem;'><b>Race</b></div>",
                unsafe_allow_html=True,
            )
            fig = plot_bar_chart(outlier_population_by_race, "PERCENTAGE", "RACE", "")
            st.plotly_chart(fig, use_container_width=True)
            st.markdown(
                "<div style='text-align:center; font-size:1.2rem;'><b>Percentage</b></div>",
                unsafe_allow_html=True,
            )

if __name__ == "__main__":
    main()