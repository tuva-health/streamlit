import sys
from pathlib import Path
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

sys.path.append(str(Path(__file__).resolve().parents[3]))

from utils import (
    round_nearest_int, 
    format_large_number
)
from shared import path_utils
from csv_data import (
    get_metrics_data_csv,
    get_member_count,
    get_member_months_count,
    get_v24_risk_score_csv,
    get_outlier_population_by_race_csv,
    get_outlier_population_by_state_csv,
)

# Add the repo root (analytics/) to sys.path so we can import shared modules
path_utils.add_repo_to_path(levels_up=3)

def display_metrics(avg_hcc_risk_score, year):
    """Display summary metrics in columns."""
    metrics_data = get_metrics_data_csv(year)
    total_outlier_members = get_member_count(year)
    total_member_months = get_member_months_count(year)

    total_members = metrics_data.get("TOTAL_COUNT", 0)
    total_paid_amount_val = metrics_data.get("TOTAL_PAID_AMOUNT", 0)
    total_paid_amount = format_large_number(total_paid_amount_val).strip()
    total_outlier_paid_val = metrics_data.get("TOTAL_OUTLIER_PAID", 0)
    total_outlier_paid = format_large_number(total_outlier_paid_val).strip()
    total_encounters = metrics_data.get("TOTAL_ENCOUNTERS", 0)
    female_count = metrics_data.get("FEMALE_COUNT", 0)
    mean_age = metrics_data.get("MEAN_AGE", 0)
    outlier_threshold = metrics_data.get("OUTLIER_THRESHOLD", 0)

    percent_female = (female_count / total_outlier_members) * 100 if total_outlier_members else 0
    encounter_per_1000 = (total_encounters / total_member_months) * 12000 if total_member_months else 0
    paid_per_encounter = (total_outlier_paid_val / total_encounters) if total_encounters else 0
    paid_pmpm = (total_outlier_paid_val / total_member_months) if total_member_months else 0

    col1, col2, col3, col5 = st.columns([2, 2, 2, 6], gap="small")
    with col1:
        st.metric("Members", f"{total_outlier_members:,}", border=True)
        st.metric("Avg HCC Risk Score", f"{avg_hcc_risk_score:.2f}", border=True)
        st.metric("Encounters / 1000", f"{round(encounter_per_1000):,}", border=True)

    with col2:
        st.metric("Percent Female", f"{percent_female:.2f}%", border=True)
        st.metric("Paid Amount", total_outlier_paid, border=True)
        st.metric("Paid / Encounter", f"${paid_per_encounter:,.2f}", border=True)

    with col3:
        st.metric("Mean Age", f"{round(mean_age):,}", border=True)
        st.metric("Paid PMPM", f"${round(paid_pmpm):,}", border=True)

    with col5:
        st.markdown(
            f"""
                **Inclusion Criteria:**  
                All beneficiaries with annual claim costs > 2 std dev from mean (${outlier_threshold:,.2f})
            """
        )
        member_col, amount_col = st.columns([1, 1], gap="small")
        with member_col:
            st.html(f"""
                <div>
                    <b>Total Members:</b> {total_members:,}<br>
                    <b>Outlier Member Count:</b> {total_outlier_members:,}<br>
                    <b>Outlier Member Ratio:</b> {total_outlier_members / total_members * 100:,.2f}%
                </div>
            """)
        with amount_col:
            st.html(f"""
                <div>
                    <b>Total Paid Amount:</b> {total_paid_amount}<br>
                    <b>Outlier Paid Amount:</b> {total_outlier_paid}<br>
                    <b>Outlier Amount Ratio:</b> {total_outlier_paid_val / total_paid_amount_val * 100:,.2f}%
                </div>
            """)

        st.markdown(
        """
            <style>
                [data-testid="stMetricValue"] {
                    font-size: 14px;
                    font-weight: 700;
                }
                [data-testid="stVerticalBlock"] {
                    gap: 0.5rem;
                }
            </style>
        """,
            unsafe_allow_html=True,
        )

def plot_bar_chart(df, x, y, title, height=650):
    """Create a horizontal bar chart with Plotly, showing full labels and scroll if needed."""
    # Format text labels conditionally
    text_labels = [f"{v:.1f}%" if x == "PERCENTAGE" else f"{int(v):,}" for v in df[x]]

    fig = px.bar(
        df,
        x=x,
        y=y,
        orientation="h",
        text=text_labels,
        height=height,
    )
    fig.update_layout(
        showlegend=False,
        margin=dict(t=40, r=80, b=40, l=120),
        title=title,
        xaxis=dict(showticklabels=False),
        yaxis=dict(
            automargin=True,
            tickfont=dict(size=13)
        )
    )
    fig.update_traces(
        marker_color="#64B0E1",
        textposition="outside",
        cliponaxis=False
    )
    return fig



def plot_risk_scores(risk_scores):
    """Plot risk scores distribution."""
    min_val = risk_scores.get("V24_RISK_MIN", 0.0)
    median_val = risk_scores.get("V24_RISK_MEDIAN", 0.0)
    max_val = risk_scores.get("V24_RISK_MAX", 0.0)

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
    year = st.session_state.get("selected_year") if "selected_year" in st.session_state else None

    outlier_population_by_state = get_outlier_population_by_state_csv(year)
    outlier_population_by_race = get_outlier_population_by_race_csv(year)
    v24_risk_scores = get_v24_risk_score_csv(year)

    st.header("Outlier Cost Driver Dashboard", divider="grey")
    st.markdown(
        f"This dashboard presents key metrics and visualizations for outlier cost drivers in the year {year}."
    )

    avg_hcc_risk_score = v24_risk_scores.get("V24_RISK_MEAN", 0.0)
    display_metrics(avg_hcc_risk_score, year)

    with st.container():
        graph1, graph2 = st.columns([1, 1], gap="large")
with graph1:
    fig = plot_bar_chart(outlier_population_by_state, "PERCENTAGE", "STATE", "Outlier Population by State", 1200)
    st.markdown('<div style="height: 500px; overflow-y: auto;">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
        with graph2:
            fig = plot_bar_chart(outlier_population_by_race, "PERCENTAGE", "RACE", "Outlier Population by Race")
            st.plotly_chart(fig, use_container_width=True)

            risk_score_fig = plot_risk_scores(v24_risk_scores)
            st.plotly_chart(risk_score_fig, use_container_width=True)

if __name__ == "__main__":
    main()
