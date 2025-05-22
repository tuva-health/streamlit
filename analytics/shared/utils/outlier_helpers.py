import streamlit as st

@st.cache_data
def get_outlier_population_by_race(_conn: str, year: str):
    return _conn.query(f"""
        SELECT 
            RACE
            , COUNT(DISTINCT MEMBER_ID) AS MEMBER_COUNT
            , CONCAT(ROUND(
                COUNT(DISTINCT MEMBER_ID) * 100.0 / 
                SUM(COUNT(DISTINCT MEMBER_ID)) OVER (), 2
            ), '%') AS PERCENTAGE 
        FROM DEV_RAJAT.TEST.OUTLIER_MEMBER_MONTHS WHERE YEAR = {year} AND RACE IS NOT NULL GROUP BY RACE;
    """)

@st.cache_data
def get_outlier_population_by_state(_conn: str, year: str):
    return _conn.query(f"""
        SELECT 
            STATE
            , COUNT(DISTINCT MEMBER_ID) AS MEMBER_COUNT
            , CONCAT(ROUND(
                COUNT(DISTINCT MEMBER_ID) * 100.0 / 
                SUM(COUNT(DISTINCT MEMBER_ID)) OVER (), 2
            ), '%') AS PERCENTAGE 
        FROM DEV_RAJAT.TEST.OUTLIER_MEMBER_MONTHS WHERE YEAR = {year} AND STATE IS NOT NULL GROUP BY STATE;
    """)