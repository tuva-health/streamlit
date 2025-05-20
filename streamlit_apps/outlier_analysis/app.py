import streamlit as st

st.set_page_config(page_icon="assets/tuva_icon.ico", layout="wide")

# Display Logo
st.logo("assets/tuva_logo.png", size="large")

# Importing pages for navigation
dashboard_page = st.Page("pages/dashboard.py", title="Dashboard")

# Setup navigation
app = st.navigation([dashboard_page])

app.run()
