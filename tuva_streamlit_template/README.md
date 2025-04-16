# TUVA Streamlit Dashboard

A TUVA application built with Streamlit for analyzing Claim data. The primary data source is Snowflake.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Setup & Installation](#setup--installation)
  - [1. Create a Virtual Environment & Install Dependencies](#1-create-a-virtual-environment--install-dependencies)
  - [2. Configure Snowflake Credentials](#2-configure-snowflake-credentials)
- [Running the Application](#running-the-application)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Prerequisites
- Python (>=3.8, <3.13) installed on your system
- An active Snowflake account with necessary access permissions
- `pip` package manager installed
- Virtual environment tool (`venv` or `virtualenv`)
- Git (to clone the repository)

## Setup & Installation

### 1️⃣ Clone the Repository

Before setting up the project, clone the repository to your local machine:

```sh
git clone https://github.com/rajat-maitri/claim_streamlit.git
cd claim_streamlit
```


### 2️⃣ Create a Virtual Environment & Install Dependencies

#### **Windows (Command Prompt or PowerShell)**
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

#### **Mac/Linux (Terminal)**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3️⃣ Configure Snowflake Credentials

#### Step 1: Retrieve Snowflake Credentials
1. Log in to your Snowflake account.
2. Click on your profile icon at the bottom left of the Snowflake dashboard.
3. Under the "Account" section, expand your unique account ID.
4. Click on "View Account Details." A dialog box will appear.
5. Navigate to the "Config File" tab.
6. Select the warehouse, database, and connection method. Choose "Web Browser" as the connection method for now.
7. Save the generated credentials.

#### Step 2: Store Credentials in Streamlit Secrets
Create a `.streamlit/secrets.toml` file in the root directory and store your credentials: A `.streamlit/secrets-sample.toml` file is added for the reference.

```toml
# .streamlit/secrets.toml

[snowflake]
user = "your_username"
account = "your_account"
warehouse = "your_warehouse"
database = "your_database"
schema = "your_schema"
authenticator = "your_authenticator"
```
🚨 **DO NOT** commit this file to version control. It is ignored via `.gitignore`.

## Running the Application
Start the Streamlit app by running:
```bash
streamlit run app.py
```
This will launch the app in your default browser at [http://localhost:8501](http://localhost:8501).

## Note
If `externalbrowser` is set as the authenticator in the `.streamlit/secrets.toml` file, you must log in through your browser. When the app starts, a new tab will open for authentication. Ensure that you use the same browser where your Snowflake account is already logged in.

If the authentication page opens in a different browser, copy the URL and paste it into the browser where your Snowflake account is logged in. Once logged in successfully, close the authentication tab and return to the Streamlit app tab to continue using the application. 

## Usage
- Use the dashboard to analyze claims data.
- Filter and visualize data retrieved from Snowflake.

## Troubleshooting
- If dependencies fail to install, ensure `pip` is updated:
  ```bash
  pip install --upgrade pip
  ```
- If you encounter authentication issues, verify your Snowflake credentials in `.streamlit/secrets.toml`.
- For permission errors, check that your Snowflake account has the required access.

## License
Copyright © 2025 The Tuva Project.