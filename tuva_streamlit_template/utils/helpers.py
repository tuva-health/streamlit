import streamlit as st


@st.cache_data
def get_table_data(_conn):
    return _conn.query("""
        SELECT
            MEDICAL_CLAIM_ID,
            CLAIM_ID,
            CLAIM_LINE_NUMBER,
            ENCOUNTER_ID,
            ENCOUNTER_TYPE,
            ENCOUNTER_GROUP,
            CLAIM_TYPE,
            PERSON_ID,
            MEMBER_ID,
            PAYER,
            PLAN,
            CLAIM_START_DATE,
            CLAIM_END_DATE,
            CLAIM_LINE_START_DATE,
            CLAIM_LINE_END_DATE,
            SERVICE_CATEGORY_1,
            SERVICE_CATEGORY_2,
            SERVICE_CATEGORY_3,
            PLACE_OF_SERVICE_CODE,
            PLACE_OF_SERVICE_DESCRIPTION,
            SERVICE_UNIT_QUANTITY,
            HCPCS_CODE,
            HCPCS_MODIFIER_1,
            HCPCS_MODIFIER_2,
            HCPCS_MODIFIER_3,
            HCPCS_MODIFIER_4,
            HCPCS_MODIFIER_5,
            RENDERING_ID,
            RENDERING_NAME,
            BILLING_ID,
            BILLING_TIN,
            PAID_DATE,
            PAID_AMOUNT,
            ALLOWED_AMOUNT,
            CHARGE_AMOUNT,
            COINSURANCE_AMOUNT,
            COPAYMENT_AMOUNT,
            DEDUCTIBLE_AMOUNT,
            TOTAL_COST_AMOUNT,
            IN_NETWORK_FLAG,
            ENROLLMENT_FLAG,
            DATA_SOURCE
        FROM DEV_PAUL.TEST.TEST_TABLE LIMIT 1000
    """)