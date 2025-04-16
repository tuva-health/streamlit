import streamlit as st

st.set_page_config(page_icon="assets/tuva_icon.ico", layout="wide")

# Display Logo
st.logo("assets/tuva_logo.png", size="large")

# Importing pages for navigation
dashboard_page = st.Page("pages/dashboard.py", title="Dashboard")
claim_amount_page = st.Page("pages/claim_amount.py", title="Claim Amount")

# Setup navigation
app = st.navigation([dashboard_page, claim_amount_page])

app.run()
