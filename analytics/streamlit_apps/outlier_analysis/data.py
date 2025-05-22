import streamlit as st


@st.cache_data
def get_member_count(_conn):
    return _conn.query("SELECT COUNT(DISTINCT MEMBER_ID) as total FROM DEV_SAUGAT.TEST.OUTLIER_MEMBER_MONTHS").iloc[0]['TOTAL']


@st.cache_data
def get_encounter_count(_conn):
    return _conn.query("SELECT COUNT(DISTINCT ENCOUNTER_ID) as total FROM DEV_SAUGAT.TEST.outlier_claims_agg").iloc[0]['TOTAL']


@st.cache_data
def get_pmpm_by_encounter_group(_conn):
    member_count = get_member_count(_conn)
    return _conn.query(f"""
        SELECT
            encounter_group,
            SUM(PAID_AMOUNT) / {member_count} AS PMPM
        FROM DEV_SAUGAT.TEST.outlier_claims_agg
        GROUP BY encounter_group ORDER BY encounter_group DESC
    """)


@st.cache_data
def get_encounters_per_1000_by_encounter_group(_conn):
    member_count = get_member_count(_conn)
    return _conn.query(f"""
        SELECT
            encounter_group,
            COUNT(DISTINCT ENCOUNTER_ID) * 12000.0 / {member_count} AS ENCOUNTERS_PER_1000
        FROM DEV_SAUGAT.TEST.outlier_claims_agg
        GROUP BY encounter_group ORDER BY encounter_group DESC
    """)


@st.cache_data
def get_paid_per_encounter_by_encounter_group(_conn):
    encounter_count = get_encounter_count(_conn)
    return _conn.query(f"""
        SELECT
            encounter_group,
            SUM(PAID_AMOUNT) / {encounter_count} AS PAID_PER_ENCOUNTER
        FROM DEV_SAUGAT.TEST.outlier_claims_agg
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
        FROM DEV_SAUGAT.TEST.outlier_claims_agg
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
        FROM DEV_SAUGAT.TEST.outlier_claims_agg
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
        FROM DEV_SAUGAT.TEST.outlier_claims_agg
        GROUP BY encounter_group, encounter_type
        ORDER BY encounter_type DESC
    """)