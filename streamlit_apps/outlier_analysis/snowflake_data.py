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
def get_total_members_count(_conn: str, year: str):
    return _conn.query(f"SELECT COUNT(DISTINCT MEMBER_ID) as total FROM CORE.MEMBER_MONTHS WHERE YEAR_MONTH BETWEEN {year}01 AND {year}12").iloc[0]['TOTAL']

@st.cache_data
def get_outlier_members_count(_conn: str, year: str):
    return _conn.query(f"SELECT COUNT(DISTINCT MEMBER_ID) as total FROM OUTLIER_MEMBER_MONTHS WHERE YEAR={year}").iloc[0]['TOTAL']

@st.cache_data
def get_encounter_count(_conn: str, year: str):
    return _conn.query(f"SELECT COUNT(DISTINCT ENCOUNTER_ID) as total FROM OUTLIER_CLAIMS_AGG WHERE INCR_YEAR={year}").iloc[0]['TOTAL']

@st.cache_data
def get_pmpm_by_encounter_group(_conn: str, year: str):
    member_count = get_outlier_members_count(_conn, year)
    return _conn.query(f"""
        SELECT
            ENCOUNTER_GROUP,
            SUM(PAID_AMOUNT) / {member_count} AS PMPM
        FROM OUTLIER_CLAIMS_AGG
        WHERE INCR_YEAR={year}
        GROUP BY ENCOUNTER_GROUP

        UNION ALL

        SELECT
            'Grand Total' AS ENCOUNTER_GROUP,
            SUM(PAID_AMOUNT) / {member_count} AS PMPM
        FROM OUTLIER_CLAIMS_AGG
        WHERE INCR_YEAR={year}

        ORDER BY PMPM
    """)


@st.cache_data
def get_encounters_per_1000_by_encounter_group(_conn: str, year: str):
    member_count = get_outlier_members_count(_conn, year)
    return _conn.query(f"""
        SELECT
            ENCOUNTER_GROUP,
            (COUNT(DISTINCT ENCOUNTER_ID) * 12000.0) / {member_count} AS ENCOUNTERS_PER_1000
        FROM OUTLIER_CLAIMS_AGG
        WHERE INCR_YEAR={year}
        GROUP BY ENCOUNTER_GROUP

        UNION ALL

        SELECT
            'Grand Total' AS ENCOUNTER_GROUP,
            (COUNT(DISTINCT ENCOUNTER_ID) * 12000.0) / {member_count} AS ENCOUNTERS_PER_1000
        FROM OUTLIER_CLAIMS_AGG
        WHERE INCR_YEAR={year}
    """)


@st.cache_data
def get_paid_per_encounter_by_encounter_group(_conn: str, year: str):
    encounter_count = get_encounter_count(_conn, year)
    return _conn.query(f"""
        SELECT
            ENCOUNTER_GROUP,
            CASE 
                WHEN COUNT(DISTINCT ENCOUNTER_ID) = 0 THEN 0 
                ELSE SUM(PAID_AMOUNT) / COUNT(DISTINCT ENCOUNTER_ID)
            END AS PAID_PER_ENCOUNTER
        FROM OUTLIER_CLAIMS_AGG
        WHERE INCR_YEAR={year}
        GROUP BY ENCOUNTER_GROUP

        UNION ALL

        SELECT
            'Grand Total' AS ENCOUNTER_GROUP,
            CASE WHEN {encounter_count} = 0 THEN 0 ELSE SUM(PAID_AMOUNT) / {encounter_count} END
        FROM OUTLIER_CLAIMS_AGG
        WHERE INCR_YEAR={year}
    """)

@st.cache_data
def get_pmpm_by_encounter_type(_conn: str, year: str):
    member_count = get_outlier_members_count(_conn, year)
    return _conn.query(f"""
        SELECT
            ENCOUNTER_GROUP,
            ENCOUNTER_TYPE,
            SUM(PAID_AMOUNT) / {member_count} AS PMPM
        FROM OUTLIER_CLAIMS_AGG
        WHERE INCR_YEAR={year}
        GROUP BY ENCOUNTER_GROUP, ENCOUNTER_TYPE

        UNION ALL

        SELECT
            'Grand Total' AS ENCOUNTER_GROUP,
            'Grand Total' AS ENCOUNTER_TYPE,
            SUM(PAID_AMOUNT) / {member_count} AS PMPM
        FROM OUTLIER_CLAIMS_AGG
        WHERE INCR_YEAR={year}
        ORDER BY PMPM
    """)


@st.cache_data
def get_encounters_per_1000_by_encounter_type(_conn: str, year: str):
    member_count = get_outlier_members_count(_conn, year)
    return _conn.query(f"""
        SELECT
            ENCOUNTER_GROUP,
            ENCOUNTER_TYPE,
            COUNT(DISTINCT ENCOUNTER_ID) * 12000.0 / {member_count} AS ENCOUNTERS_PER_1000
        FROM OUTLIER_CLAIMS_AGG
        WHERE INCR_YEAR={year}
        GROUP BY ENCOUNTER_GROUP, ENCOUNTER_TYPE
        
        UNION ALL

        SELECT
            'Grand Total' AS ENCOUNTER_GROUP,
            'Grand Total' AS ENCOUNTER_TYPE,
            COUNT(DISTINCT ENCOUNTER_ID) * 12000.0 / {member_count} AS ENCOUNTERS_PER_1000
        FROM OUTLIER_CLAIMS_AGG
        WHERE INCR_YEAR={year}
    """)


@st.cache_data
def get_paid_per_encounter_by_encounter_type(_conn: str, year: str):
    encounter_count = get_encounter_count(_conn, year)
    return _conn.query(f"""
        SELECT
            ENCOUNTER_GROUP,
            ENCOUNTER_TYPE,
            CASE 
                WHEN COUNT(DISTINCT ENCOUNTER_ID) = 0 THEN 0 
                ELSE SUM(PAID_AMOUNT) / COUNT(DISTINCT ENCOUNTER_ID)
            END AS PAID_PER_ENCOUNTER
        FROM OUTLIER_CLAIMS_AGG
        WHERE INCR_YEAR={year}
        GROUP BY ENCOUNTER_GROUP, ENCOUNTER_TYPE

        UNION ALL

        SELECT
            'Grand Total' AS ENCOUNTER_GROUP,
            'Grand Total' AS ENCOUNTER_TYPE,
            CASE WHEN {encounter_count} = 0 THEN 0 ELSE SUM(PAID_AMOUNT) / {encounter_count} END
        FROM OUTLIER_CLAIMS_AGG
        WHERE INCR_YEAR={year}
    """)

@st.cache_data
def get_pmpm_by_diagnosis_category(_conn: str, year: str):
    member_count = get_outlier_members_count(_conn, year)
    return _conn.query(f"""
        WITH category_pmpm AS (
            SELECT
                DX_CCSR_CATEGORY2,
                SUM(PAID_AMOUNT) / {member_count} AS PMPM
            FROM OUTLIER_CLAIMS_AGG
            WHERE INCR_YEAR={year}
            GROUP BY DX_CCSR_CATEGORY2
        ),
        total_pmpm AS (
            SELECT SUM(PMPM) AS total_pmpm
            FROM category_pmpm
        )

        SELECT 
            c.DX_CCSR_CATEGORY2,
            c.PMPM,
            ROUND((c.PMPM / t.total_pmpm) * 100, 1) AS PERCENT_OF_TOTAL_PMPM,
            SUM(c.PMPM) OVER (ORDER BY c.PMPM DESC) AS CUMULATIVE_PMPM
        FROM category_pmpm c
        CROSS JOIN total_pmpm t
        ORDER BY c.PMPM;
    """)

@st.cache_data
def get_pmpm_by_diagnosis(_conn: str, year: str):
    member_count = get_outlier_members_count(_conn, year)
    return _conn.query(f"""
        WITH category_pmpm AS (
            SELECT
                DX_DESCRIPTION,
                SUM(PAID_AMOUNT) / {member_count} AS PMPM
            FROM OUTLIER_CLAIMS_AGG
            WHERE INCR_YEAR={year}
            GROUP BY DX_DESCRIPTION
        ),
        total_pmpm AS (
            SELECT SUM(PMPM) AS total_pmpm
            FROM category_pmpm
        )

        SELECT 
            c.DX_DESCRIPTION,
            c.PMPM,
            ROUND((c.PMPM / t.total_pmpm) * 100, 1) AS PERCENT_OF_TOTAL_PMPM,
            SUM(c.PMPM) OVER (ORDER BY c.PMPM DESC) AS CUMULATIVE_PMPM
        FROM category_pmpm c
        CROSS JOIN total_pmpm t
        ORDER BY c.PMPM;
    """)