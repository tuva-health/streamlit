Absolutely! Here's a complete `README.md` for the `streamlit_apps/tuva_template/` folder, formatted in Markdown and ready to drop in:

---

```markdown
# Tuva Streamlit Template App

This is a ready-to-run **Streamlit app template** for analyzing healthcare claims data using the Tuva data model and Snowflake. It demonstrates best practices for structuring multipage apps, using shared helper functions, and working with Snowflake credentials securely.

---

## 📋 What This Template Includes

- ✅ **Multipage Streamlit layout** with pages in the `pages/` folder
- ✅ **Snowflake integration** using `.streamlit/secrets.toml`
- ✅ **Reusable code** via `shared/utils/helpers.py`
- ✅ **Visualizations** using Plotly and pandas
- ✅ **Custom styling** via Streamlit’s `markdown()` injection

---

## 🚀 How to Run This App

1. **Navigate to this app’s folder**:

   ```bash
   cd streamlit_apps/tuva_template
   ```

2. **(Optional but recommended) Activate your virtual environment**:

   ```bash
   source ../../.venv/bin/activate      # Mac/Linux
   .\\..\\.venv\\Scripts\\activate      # Windows
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Snowflake credentials** by creating a file:

   ```
   .streamlit/secrets.toml
   ```

   Example contents:

   ```toml
   [snowflake]
   user = "your_username"
   account = "your_account"
   warehouse = "your_warehouse"
   database = "your_database"
   schema = "your_schema"
   authenticator = "externalbrowser"
   ```

5. **Run the app**:

   ```bash
   streamlit run app.py
   ```

6. The app will open in your browser at [http://localhost:8501](http://localhost:8501)

---

## 🛠 Developer Notes

- `helpers.get_table_data()` is the default function for querying Snowflake and returning a DataFrame. It lives in `shared/utils/helpers.py`.
- Any imports from `shared/` require that you first add the project root to `sys.path`. This is handled at the top of each page using `path_utils.add_repo_to_path(levels_up=3)`.
- The `dashboard.py` and `claim_amount.py` pages each demonstrate different types of visualizations using claims data.

---

## 📁 Folder Overview

```bash
tuva_template/
├── app.py                     # Main entry point for Streamlit
├── pages/                     # Individual dashboard pages
│   ├── dashboard.py
│   └── claim_amount.py
├── requirements.txt           # Python dependencies for this app
└── .streamlit/                # Streamlit config and secrets
    └── config.toml
    └── secrets.toml (you create this)
```

---

