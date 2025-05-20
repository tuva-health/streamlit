import sys
from pathlib import Path
import streamlit as st
import plotly.express as px
import pandas as pd

# Add the repo root (analytics/) to sys.path so we can import shared modules
sys.path.append(str(Path(__file__).resolve().parents[3]))

from shared import path_utils
path_utils.add_repo_to_path(levels_up=3)

@st.cache_data
def load_data():
    data1 = pd.DataFrame(
        [
            ["AL", "12%"],
            ["AK", "8%"],
            ["AZ", "10%"],
            ["AR", "15%"],
            ["CA", "20%"],
            ["CO", "18%"],
            ["CT", "22%"],
            ["DE", "25%"],
            ["FL", "30%"],
            ["GA", "35%"]
        ],
        columns=["State", ""]
    )

    data2 = pd.DataFrame(
        [
            ["White", "12%"],
            ["Black", "8%"],
            ["Asian", "10%"],
            ["Hispanic", "15%"],
            ["Native American", "20%"],
            ["Other", "18%"],
            ["Unknown", "22%"],
            ["Mixed", "25%"],
            ["Pacific Islander", "30%"],
            ["Middle Eastern", "35%"]
        ],
        columns=["Race", ""]
    )

    return data1, data2

data1, data2 = load_data()

# --- Page Title and Description ---
st.header("Medicare LDS Outlier Cost Driver Dashboard", divider="grey")
st.markdown(
    "This dashboard presents key metrics and visualizations for outlier cost drivers in the 2020 Medicare LDS 5% Sample."
)

st.write("####") # Add blank space between sections

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


st.write("####") # Add blank space between sections

with st.container():
    graph1, graph2 = st.columns([1, 1], gap="large")
    with graph1:
        st.subheader("Outlier Population by State")
        fig = px.bar(
            data1,
            x=data1.columns[1],
            y="State",
            orientation="h",
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)


    with graph2:
        st.subheader("Outlier Population by Race")
        fig = px.bar(
            data2,
            x=data2.columns[1],
            y="Race",
            orientation="h",
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)