import streamlit as st
st.set_page_config(page_icon="assets/tuva_icon.ico", layout="wide")

st.markdown(
    """
    <style>
        [data-testid="stLogo"] {
            margin: 0px;
            max-width: unset;
            font-weight: 700;
            object-fit: fill;
        }
        [data-testid="stSidebarHeader"] {
            padding-left: 14px;
            padding-right: 14px;
        }
        .stSidebar {
            min-width: 300px;
            max-width: 300px;
            transition: min-width 0.3s ease-in-out, width 0.3s ease-in-out;
        }
        .stSidebar[aria-expanded="false"] {
            width: 0px !important;
            min-width: 0px !important;
            transition: min-width 0.3s ease-in-out, width 0.3s ease-in-out;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Display Logo
st.logo("assets/tuva_logo.png", size="large")

st.markdown(
    """
    <style>
        .stMainBlockContainer  {
            padding-left: 1rem;
            padding-right: 1rem;
            padding-top: 3rem;
            padding-bottom: 2rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Importing pages for navigation
dashboard_page = st.Page("pages/outliers_cost_driver.py", title="Outlier Cost Driver")
outliers_by_encounter_page = st.Page("pages/outliers_by_encounter.py", title="Outliers By Encounter")
outliers_by_diagnosis_page = st.Page("pages/outliers_by_diagnosis.py", title="Outliers By Diagnosis")

# Setup navigation
app = st.navigation([
    dashboard_page, outliers_by_encounter_page, outliers_by_diagnosis_page
    ], position="hidden")

# year_list = get_year_list(st.connection("snowflake"))
from csv_data import get_year_list 
year_list = get_year_list()
with st.sidebar:
    selected_year = st.selectbox(
            "Select Year",
            options=year_list,
            index=0,
            key="selected_year",
        )
    st.divider()
    st.page_link("pages/outliers_cost_driver.py", label="Outlier Cost Driver")
    st.page_link("pages/outliers_by_encounter.py", label="Outliers By Encounter")
    st.page_link("pages/outliers_by_diagnosis.py", label="Outliers By Diagnosis")

app.run()
