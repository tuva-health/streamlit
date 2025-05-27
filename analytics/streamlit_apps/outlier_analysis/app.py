import streamlit as st

st.set_page_config(page_icon="assets/tuva_icon.ico", layout="wide")

# Display Logo
st.logo("assets/tuva_logo.png", size="large")

# Importing pages for navigation
dashboard_page = st.Page("pages/outliers_cost_driver.py", title="Outlier Cost Driver")
outliers_by_encounter_page = st.Page("pages/outliers_by_encounter.py", title="Outliers By Encounter")
outliers_by_diagnosis_page = st.Page("pages/outliers_by_diagnosis.py", title="Outliers By Diagnosis")

# Setup navigation
app = st.navigation([dashboard_page, outliers_by_encounter_page, outliers_by_diagnosis_page])

app.run()
