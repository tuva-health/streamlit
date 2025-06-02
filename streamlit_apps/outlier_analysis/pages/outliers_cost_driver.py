from decimal import Decimal
import sys
from pathlib import Path
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

sys.path.append(str(Path(__file__).resolve().parents[3]))
from data import (
    get_metrics_data,
    get_mean_paid,
    get_avg_hcc_risk_score,
    get_outlier_claims_data,
    get_outlier_population_by_race,
    get_outlier_population_by_state,
    get_v24_risk_scores
)
from utils import safe_extract, round_nearest_int, format_large_number
from shared import path_utils

# Add the repo root (analytics/) to sys.path so we can import shared modules
path_utils.add_repo_to_path(levels_up=3)

def display_metrics(conn, year):
    """Display summary metrics in columns."""
   
    mean_paid = get_mean_paid(conn, year).iloc[0]
    avg_hcc_risk_score = get_avg_hcc_risk_score(conn, year).iloc[0]
    metrics_data = get_metrics_data(conn, year)
    claims_data = get_outlier_claims_data(conn, year)
    metrics_data["MEAN_PAID"] = mean_paid

    # Extract and sanitize values
    total_population = safe_extract(metrics_data.get("MEMBER_MONTHS"), default=0, as_type=int)
    female_count = safe_extract(metrics_data.get("FEMALE_COUNT"), default=0, as_type=float)
    mean_age = safe_extract(metrics_data.get("MEAN_AGE"), default="N/A", as_type=Decimal)
    mean_paid = safe_extract(metrics_data.get("MEAN_PAID"), default=0.0, as_type=float)
    total_paid = safe_extract(claims_data.get("TOTAL_PAID"), default=0.0, as_type=float)
    total_encounters = safe_extract(claims_data.get("TOTAL_ENCOUNTERS"), default=0, as_type=int)

    # Compute derived metrics safely
    percent_female = (female_count / total_population) * 100 if total_population else 0.0
    encounter_per_1000 = (total_encounters / total_population) * 12000 if total_population else 0.0
    paid_per_encounter = (total_paid / total_encounters) if total_encounters else 0.0
    paid_pmpm = (total_paid / total_population) if total_population else 0.0
    rounded_mean_age = round_nearest_int(mean_age)
    rounded_paid_pmpm = f"${round_nearest_int(paid_pmpm)}"
    rounded_encounter_per_1000 = round_nearest_int(encounter_per_1000)
    paid_per_encounter = (total_paid / total_encounters) if total_encounters else 0.0
    paid_per_encounter = f"${paid_per_encounter:,.2f}" if total_encounters else "$0.00"

    col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 4], gap="small")
    with col1:
        st.metric("Members", total_population, border=True)
        st.metric("Mean Age **(Yrs)**", rounded_mean_age, border=True)

    with col2:
        st.metric("Percent Female **(%)**", f"{percent_female:.2f}", border=True)
        st.metric("Avg HCC Risk Score", f"{avg_hcc_risk_score:.2f}", border=True)  # Replace with actual value if available

    with col3:
        st.metric("Paid Amount **($)**", format_large_number(total_paid), border=True)
        st.metric("Paid PMPM **($)**", rounded_paid_pmpm, border=True)

    with col4:
        st.metric("Encounters / 1000", rounded_encounter_per_1000, border=True)
        st.metric("Paid / Encounter **($)**", paid_per_encounter, border=True)

    with col5:
        st.markdown(
            f"""
            **Inclusion Criteria:** All beneficiaries with annual claim costs > 2 std dev from mean (${mean_paid:,.2f})
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
            marker_color= "#64B0E1",
            textposition="outside",
            texttemplate="%{x}%" if x == "PERCENTAGE" else "%{x}",
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
    year = st.session_state.get("page_selector") if "page_selector" in st.session_state else None
    try:
        conn = st.connection("snowflake")
    except Exception as e:
        st.error(f"Failed to connect to Snowflake: {e}")
        st.stop()

    outlier_population_by_state = get_outlier_population_by_state(conn, year)
    outlier_population_by_race = get_outlier_population_by_race(conn, year)
    v24_risk_scores = get_v24_risk_scores(conn, year)

    # --- Page Title and Description ---
    st.header("Outlier Cost Driver Dashboard", divider="grey")
    st.markdown(
        f"This dashboard presents key metrics and visualizations for outlier cost drivers in the year {year}."
    )

    display_metrics(conn, year)

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