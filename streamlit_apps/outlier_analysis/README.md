# Outlier Analysis App

This is a ready-to-run **Streamlit app** that uses Tuva synthetic data to visualize outliers data. It provides a multipage layout, shared helper utilities, and secure Snowflake integration, serving as a template for building robust data analysis dashboards.

---

## 📋 What This Template Includes

- ✅ **Multipage Streamlit layout** with pages in the `pages/` folder
- ✅ **Visualizations** using Plotly and pandas
- ✅ **Custom styling** via Streamlit’s `markdown()` injection

---

## 🚀 How to Run This App

1. **Navigate to this app’s folder**:

   ```bash
   cd streamlit_apps/outlier_analysis
   ```

2. **Activate your virtual environment & Install dependencies**


   #### 💻 macOS/Linux
   ```bash
   python3 -m venv .venv
   source ../../.venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

   #### 🪟 Windows
   ```bash
   python -m venv .venv
   ..\.venv\Scripts\activate
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **Run the app**:

   ```bash
   streamlit run app.py
   ```

4. The app will open in your browser at [http://localhost:8501](http://localhost:8501)

---

## 🛠 Developer Notes

- Common shared function can be stored and imported from `shared/utils/helpers.py` directory.
- Any imports from `shared/` require that you first add the project root to `sys.path`. This is handled at the top of each page using `path_utils.add_repo_to_path(levels_up=3)`.

---

## 📁 Folder Overview

```bash
outlier_analysis/
├── app.py                     # Main entry point for the Streamlit app
├── csv_data.py                # Functions to transform the CSVs to visualize data
├── data/                      # CSV files generated from Tuva synthetic data for powering the Streamlit app
│   ├── outlier_claims_agg.csv
│   └── outlier_member_months.csv
├── pages/                     # Individual dashboard pages
│   ├── dashboard.py
│   └── dashboard-2.py
├── sql/                     # SQL queries to create required tables for the CSVs
│   └── outlier_queries.sql
├── requirements.txt           # Python dependencies for this app
└── .streamlit/                # Streamlit config and secrets if required
    └── config.toml
    └── secrets.toml (you create this)
```

## 📂 Using Your Own Data

If you'd like to run the Streamlit Outlier Analysis App using your **own data**, follow these steps after successfully running your Tuva DBT project:

1. **Ensure Tuva DBT Project is Set Up**  
   You must first run your Tuva DBT project and ensure all core tables (e.g., `CORE.MEMBER_MONTHS`, `CORE.MEDICAL_CLAIM`, etc.) are materialized correctly in your data warehouse.

2. **Run the Outlier Queries**  
   Execute the SQL logic found in `outlier_queries.sql` against your data warehouse. This script will create the necessary views and tables under the `OUTLIERS` schema, including:

   - `OUTLIERS.OUTLIER_MEMBER_MONTHS`
   - `OUTLIERS.OUTLIER_CLAIMS_AGG`

3. **Export the Output as CSVs**  
   After executing the queries, export the following tables as CSVs:

   - `OUTLIERS.OUTLIER_CLAIMS_AGG` → Save as `outlier_claims_agg.csv`
   - `OUTLIERS.OUTLIER_MEMBER_MONTHS` → Save as `outlier_member_months.csv`

4. **Replace the Data in the App**  
   Place the exported CSVs in the app’s `data/` folder, replacing the existing sample files:

   ```bash
   data/
   ├── outlier_claims_agg.csv       # Replace with your exported file
   └── outlier_member_months.csv   # Replace with your exported file

5. **Run the App**  
  Now, launch the Streamlit app as described above. It will now visualize and analyze your own data instead of the synthetic Tuva data.

   ```bash
   streamlit run app.py
