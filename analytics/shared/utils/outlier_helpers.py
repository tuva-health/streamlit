import streamlit as st

@st.cache_data
def get_metrics_data(_conn: str, year: str):
    return _conn.query(f"""
        SELECT 
            COUNT(DISTINCT OM.MEMBER_ID) AS MEMBER_MONTHS
            , AVG(OM.AGE) AS MEAN_AGE
            , COUNT(DISTINCT CASE WHEN OM.SEX = 'female' THEN OM.MEMBER_ID END) AS FEMALE_COUNT
            , SUM(AC.PAID_AMOUNT) AS TOTAL_PAID
            , COUNT(DISTINCT AC.ENCOUNTER_ID) AS TOTAL_ENCOUNTERS
        FROM DEV_RAJAT.TEST.OUTLIER_MEMBER_MONTHS OM
        LEFT JOIN DEV_RAJAT.TEST.ALL_CLAIMS_AGG AC
            ON OM.MEMBER_ID = AC.MEMBER_ID
        WHERE OM.YEAR = {year};
    """)

@st.cache_data
def get_mean_paid(_conn: str, year: str):
    return _conn.query(f"""
        SELECT 
            mean_paid
        FROM DEV_RAJAT.TEST.OUTLIER_MEMBERS
        WHERE INCR_YEAR = {year}
        LIMIT 1;
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
        FROM DEV_RAJAT.TEST.OUTLIER_MEMBER_MONTHS WHERE YEAR = {year} AND RACE IS NOT NULL GROUP BY RACE;
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
        FROM DEV_RAJAT.TEST.OUTLIER_MEMBER_MONTHS WHERE YEAR = {year} AND STATE IS NOT NULL GROUP BY STATE;
    """)