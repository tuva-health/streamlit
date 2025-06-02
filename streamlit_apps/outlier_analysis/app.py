import streamlit as st
from data import get_year_list

st.set_page_config(page_icon="assets/tuva_icon.ico", layout="wide")

st.markdown(
    """
    <style>
        [data-testid="stLogo"] {
                height: 1.5rem;
                margin: 0px;
                max-width: calc(260px - 4.75rem);
                font-weight: 700;
                object-fit: fill;
            }
    </style>
    """,
    unsafe_allow_html=True
)

# Display Logo
st.logo("assets/tuva_logo.png", size="large")

# Importing pages for navigation
dashboard_page = st.Page("pages/outliers_cost_driver.py", title="Outlier Cost Driver")
outliers_by_encounter_page = st.Page("pages/outliers_by_encounter.py", title="Outliers By Encounter")
outliers_by_diagnosis_page = st.Page("pages/outliers_by_diagnosis.py", title="Outliers By Diagnosis")

# Setup navigation
app = st.navigation([
    dashboard_page, outliers_by_encounter_page, outliers_by_diagnosis_page
    ], position="hidden")

year_list = get_year_list(st.connection("snowflake"))
with st.sidebar:
    selected_year = st.selectbox(
            "Select Year",
            options=year_list,
            index=0,
            key="page_selector"
        )
    st.divider()
    st.page_link("pages/outliers_cost_driver.py", label="Outlier Cost Driver")
    st.page_link("pages/outliers_by_encounter.py", label="Outliers By Encounter")
    st.page_link("pages/outliers_by_diagnosis.py", label="Outliers By Diagnosis")

app.run()
