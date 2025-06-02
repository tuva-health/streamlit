import streamlit as st

# App.py

@st.cache_data
def get_year_list(_conn: str):
    return _conn.query("""
        SELECT DISTINCT YEAR
        FROM OUTLIER_MEMBER_MONTHS
        ORDER BY YEAR DESC;
    """)['YEAR'].tolist()

# OUTLIER COST DRIVER

@st.cache_data
def get_metrics_data(_conn: str, year: str):
    return _conn.query(f"""
        SELECT 
            COUNT(DISTINCT OM.MEMBER_ID) AS MEMBER_MONTHS
            , AVG(OM.AGE) AS MEAN_AGE
            , COUNT(DISTINCT CASE WHEN OM.SEX = 'female' THEN OM.MEMBER_ID END) AS FEMALE_COUNT
        FROM OUTLIER_MEMBER_MONTHS OM
        WHERE OM.YEAR = {year};
    """)

@st.cache_data
def get_outlier_claims_data(_conn: str, year: str):
    return _conn.query(f"""
        SELECT 
            SUM(PAID_AMOUNT) AS TOTAL_PAID
            , COUNT(DISTINCT ENCOUNTER_ID) AS TOTAL_ENCOUNTERS
        FROM OUTLIER_CLAIMS_AGG
        WHERE INCR_YEAR = {year};
    """)


@st.cache_data
def get_mean_paid(_conn: str, year: str):
    return _conn.query(f"""
        SELECT 
            mean_paid
        FROM OUTLIER_MEMBERS
        WHERE INCR_YEAR = {year}
        LIMIT 1;
    """).iloc[0]

@st.cache_data
def get_avg_hcc_risk_score(_conn: str, year: str):
    return _conn.query(f"""
        SELECT 
            AVG(V24_RISK_SCORE) AS AVG_RISK_SCORE
        FROM OUTLIER_MEMBER_MONTHS
        WHERE YEAR = {year} AND V24_RISK_SCORE IS NOT NULL;;
    """).iloc[0]

@st.cache_data
def get_outlier_population_by_race(_conn: str, year: str):
    return _conn.query(f"""
        SELECT 
            RACE
            , COUNT(DISTINCT MEMBER_ID) AS MEMBER_COUNT
            , ROUND(
                COUNT(DISTINCT MEMBER_ID) * 100.0 / 
                SUM(COUNT(DISTINCT MEMBER_ID)) OVER (), 2
            ) AS PERCENTAGE 
        FROM OUTLIER_MEMBER_MONTHS WHERE YEAR = {year} AND RACE IS NOT NULL GROUP BY RACE
        ORDER BY PERCENTAGE;
    """)

@st.cache_data
def get_outlier_population_by_state(_conn: str, year: str):
    return _conn.query(f"""
        SELECT 
            STATE
            , COUNT(DISTINCT MEMBER_ID) AS MEMBER_COUNT
            , ROUND(
                COUNT(DISTINCT MEMBER_ID) * 100.0 / 
                SUM(COUNT(DISTINCT MEMBER_ID)) OVER (), 2
            ) AS PERCENTAGE 
        FROM OUTLIER_MEMBER_MONTHS WHERE YEAR = {year} AND STATE IS NOT NULL GROUP BY STATE
        ORDER BY PERCENTAGE;
    """)

@st.cache_data
def get_v24_risk_scores(_conn: str, year: str):
    return _conn.query(f"""
        SELECT 
            DISTINCT(MEMBER_ID)
            , V24_RISK_SCORE AS RISK_SCORE
        FROM OUTLIER_MEMBER_MONTHS
        WHERE YEAR = {year} AND RISK_SCORE IS NOT NULL;
    """)


# OUTLIERS BY ENCOUNTER

@st.cache_data
def get_member_count(_conn):
    return _conn.query("SELECT COUNT(DISTINCT MEMBER_ID) as total FROM OUTLIER_MEMBER_MONTHS").iloc[0]['TOTAL']


@st.cache_data
def get_encounter_count(_conn):
    return _conn.query("SELECT COUNT(DISTINCT ENCOUNTER_ID) as total FROM outlier_claims_agg").iloc[0]['TOTAL']


@st.cache_data
def get_pmpm_by_encounter_group(_conn):
    member_count = get_member_count(_conn)
    return _conn.query(f"""
        SELECT
            encounter_group,
            SUM(PAID_AMOUNT) / {member_count} AS PMPM
        FROM outlier_claims_agg
        GROUP BY encounter_group ORDER BY encounter_group DESC
    """)


@st.cache_data
def get_encounters_per_1000_by_encounter_group(_conn):
    member_count = get_member_count(_conn)
    return _conn.query(f"""
        SELECT
            encounter_group,
            COUNT(DISTINCT ENCOUNTER_ID) * 12000.0 / {member_count} AS ENCOUNTERS_PER_1000
        FROM outlier_claims_agg
        GROUP BY encounter_group ORDER BY encounter_group DESC
    """)


@st.cache_data
def get_paid_per_encounter_by_encounter_group(_conn):
    encounter_count = get_encounter_count(_conn)
    return _conn.query(f"""
        SELECT
            encounter_group,
            SUM(PAID_AMOUNT) / {encounter_count} AS PAID_PER_ENCOUNTER
        FROM outlier_claims_agg
        GROUP BY encounter_group ORDER BY encounter_group DESC
    """)

@st.cache_data
def get_pmpm_by_encounter_type(_conn):
    member_count = get_member_count(_conn)
    return _conn.query(f"""
        SELECT
            encounter_group,
            encounter_type,
            SUM(PAID_AMOUNT) / {member_count} AS PMPM
        FROM outlier_claims_agg
        GROUP BY encounter_group, encounter_type
        ORDER BY encounter_type DESC
    """)


@st.cache_data
def get_encounters_per_1000_by_encounter_type(_conn):
    member_count = get_member_count(_conn)
    return _conn.query(f"""
        SELECT
            encounter_group,
            encounter_type,
            COUNT(DISTINCT ENCOUNTER_ID) * 12000.0 / {member_count} AS ENCOUNTERS_PER_1000
        FROM outlier_claims_agg
        GROUP BY encounter_group, encounter_type
        ORDER BY encounter_type DESC
    """)


@st.cache_data
def get_paid_per_encounter_by_encounter_type(_conn):
    encounter_count = get_encounter_count(_conn)
    return _conn.query(f"""
        SELECT
            encounter_group,
            encounter_type,
            SUM(PAID_AMOUNT) / {encounter_count} AS PAID_PER_ENCOUNTER
        FROM outlier_claims_agg
        GROUP BY encounter_group, encounter_type
        ORDER BY encounter_type DESC
    """)