import streamlit as st
import numpy as np
import pandas as pd


@st.cache_data
def load_data(file):
    try:
        data = pd.read_csv(file)
        return data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()
    

agg_claim_path = "data/outlier_claims_agg.csv"
outlier_claims_agg_data = load_data(agg_claim_path)

outlier_member_path = "data/outlier_member_months.csv"
outlier_member_months_data = load_data(outlier_member_path)

def get_year_list():
    """Get the list of years available in the dataset."""
    return sorted(outlier_member_months_data['YEAR'].unique().tolist(), reverse=True)

@st.cache_data
def get_member_count(selected_year):
    """Get the total number of outlier members for the selected year."""
    df_by_year = outlier_member_months_data[outlier_member_months_data['YEAR'].eq(selected_year)]
    member_count = 0
    if not df_by_year.empty:
        member_count = df_by_year['MEMBER_ID'].nunique()
    return member_count

@st.cache_data
def get_metrics_data_csv(selected_year):
    """Get the metrics data for the selected year."""
    if selected_year:
        member_months_by_year = outlier_member_months_data[outlier_member_months_data['YEAR'].eq(selected_year)]

        mean_age = member_months_by_year['AGE'].mean()
        female_count = member_months_by_year[member_months_by_year["SEX"] == 'female']['MEMBER_ID'].nunique()
        
        claims_agg_by_year = outlier_claims_agg_data[outlier_claims_agg_data['INCR_YEAR'].eq(selected_year)]

        total_count = claims_agg_by_year['TOTAL_MEMBERS'].iloc[0]
        total_paid = claims_agg_by_year['PAID_AMOUNT'].sum()
        mean_paid = claims_agg_by_year['MEAN_PAID'].iloc[0]
        total_encounters = claims_agg_by_year['ENCOUNTER_ID'].nunique()

        return {
            "TOTAL_COUNT": total_count,
            "TOTAL_ENCOUNTERS": total_encounters,
            "TOTAL_PAID": total_paid,
            "MEAN_PAID": mean_paid,
            "MEAN_AGE": mean_age, 
            "FEMALE_COUNT": female_count
            }
    
    return {
        "TOTAL_COUNT": 0, 
        "TOTAL_ENCOUNTERS": 0,
        "TOTAL_PAID": 0,
        "MEAN_AGE": 0, 
        "MEAN_PAID": 0,
        "FEMALE_COUNT": 0
        }

@st.cache_data
def get_v24_risk_score_csv(selected_year):
    """Get HCC risk score detail for the selected year."""
    df_by_year = outlier_member_months_data[outlier_member_months_data['YEAR'].eq(selected_year)]

    if not df_by_year.empty:
        v24_risk_mean = df_by_year['V24_RISK_SCORE'].mean()
        v24_risk_median = df_by_year['V24_RISK_SCORE'].median()
        v24_risk_min = df_by_year['V24_RISK_SCORE'].min()
        v24_risk_max = df_by_year['V24_RISK_SCORE'].max()
    else:
        v24_risk_mean = v24_risk_median = v24_risk_min = v24_risk_max = 0.0

    return {
        "V24_RISK_MEAN": v24_risk_mean,
        "V24_RISK_MEDIAN": v24_risk_median,
        "V24_RISK_MIN": v24_risk_min,
        "V24_RISK_MAX": v24_risk_max
    }

@st.cache_data
def get_outlier_population_by_race_csv(selected_year):
    """Get the outlier population by Race for the selected year."""
    df_by_year = outlier_member_months_data[outlier_member_months_data['YEAR'].eq(selected_year)]
    filtered_data = df_by_year[(df_by_year["RACE"].notnull())]
    if not filtered_data.empty:
        population_by_race = filtered_data.groupby('RACE')['MEMBER_ID'].nunique().reset_index(name='MEMBER_COUNT')
        total_members = population_by_race['MEMBER_COUNT'].sum()
        population_by_race['PERCENTAGE'] = (population_by_race['MEMBER_COUNT'] / total_members * 100).round(2)
        population_by_race = population_by_race.sort_values('PERCENTAGE')
        
    return population_by_race

@st.cache_data
def get_outlier_population_by_state_csv(selected_year):
    """Get the outlier population by State for the selected year."""
    df_by_year = outlier_member_months_data[outlier_member_months_data['YEAR'].eq(selected_year)]
    filtered_data = df_by_year[(outlier_member_months_data["STATE"].notnull())]
    if not filtered_data.empty:
        population_by_state = filtered_data.groupby('STATE')['MEMBER_ID'].nunique().reset_index(name='MEMBER_COUNT')
        total_members = population_by_state['MEMBER_COUNT'].sum()
        population_by_state['PERCENTAGE'] = (population_by_state['MEMBER_COUNT'] / total_members * 100).round(2)
        population_by_state = population_by_state.sort_values('PERCENTAGE')
        
    return population_by_state

# OUTLIERS BY ENCOUNTER #

@st.cache_data
def get_encounter_count(selected_year):
    """Get the total number of encounters for the selected year."""
    df_by_year = outlier_claims_agg_data[outlier_claims_agg_data['INCR_YEAR'].eq(selected_year)]
    encounter_count = 0
    if not df_by_year.empty:
        encounter_count = df_by_year['ENCOUNTER_ID'].nunique()
    return encounter_count


@st.cache_data
def get_pmpm_and_encounters_by_group_csv(selected_year):
    """Get PMPM and ENCOUNTERS_PER_1000 and PAID_PER_ENCOUNTER by encounter group for the selected year."""
    member_count = get_member_count(selected_year)
    encounter_count = get_encounter_count(selected_year)
    
    df_by_year = outlier_claims_agg_data[outlier_claims_agg_data['INCR_YEAR'].eq(selected_year)]

    if member_count == 0 or df_by_year.empty:
        return pd.DataFrame(columns=['ENCOUNTER_GROUP', 'PMPM', 'ENCOUNTERS_PER_1000', 'PAID_PER_ENCOUNTER'])
    
    df_by_year["ENCOUNTER_GROUP"] = df_by_year["ENCOUNTER_GROUP"].fillna('null')
   
    combined_df = (
        df_by_year
        .groupby('ENCOUNTER_GROUP', as_index=False)
        .agg(
            PAID_AMOUNT=('PAID_AMOUNT', 'sum'),
            ENCOUNTER_COUNT=('ENCOUNTER_ID', 'nunique')
        )
        .assign(
            PMPM=lambda df: df['PAID_AMOUNT'] / member_count,
            ENCOUNTERS_PER_1000=lambda df: df['ENCOUNTER_COUNT'] * 12000.0 / member_count,
            PAID_PER_ENCOUNTER=lambda df: np.where(
                df['ENCOUNTER_COUNT'] == 0, 0.0, df['PAID_AMOUNT'] / df['ENCOUNTER_COUNT']
            )
        )
        [['ENCOUNTER_GROUP', 'PMPM', 'PAID_AMOUNT', 'ENCOUNTERS_PER_1000', 'PAID_PER_ENCOUNTER']]
    )

    # Add Grand Total row
    grand_total = {
        'ENCOUNTER_GROUP': 'Grand Total',
        'PMPM': combined_df['PMPM'].sum(skipna=True),
        'ENCOUNTERS_PER_1000': combined_df['ENCOUNTERS_PER_1000'].sum(skipna=True),
        'PAID_PER_ENCOUNTER': combined_df['PAID_AMOUNT'].sum(skipna=True) / encounter_count if encounter_count else 0.0
    }

    result = pd.concat([combined_df, pd.DataFrame([grand_total])], ignore_index=True).dropna(subset=['ENCOUNTER_GROUP'])
    result = result.sort_values(by='PMPM', ascending=True, ignore_index=True)

    return result


@st.cache_data
def get_pmpm_and_encounters_by_type_csv(selected_year):
    """Get PMPM and ENCOUNTERS_PER_1000 by encounter type for the selected year."""
    member_count = get_member_count(selected_year)
    encounter_count = get_encounter_count(selected_year)

    df_by_year = outlier_claims_agg_data[outlier_claims_agg_data['INCR_YEAR'].eq(selected_year)]

    if member_count == 0 or df_by_year.empty:
        return pd.DataFrame(columns=['ENCOUNTER_GROUP', 'ENCOUNTER_TYPE', 'PAID_AMOUNT', 'PMPM', 'ENCOUNTERS_PER_1000', 'PAID_PER_ENCOUNTER'])
    
    df_by_year.fillna({'ENCOUNTER_GROUP': 'null', 'ENCOUNTER_TYPE': 'null'}, inplace=True)

    combined_df = (
        df_by_year
        .groupby(['ENCOUNTER_GROUP', 'ENCOUNTER_TYPE'], as_index=False)
        .agg(
            PAID_AMOUNT=('PAID_AMOUNT', 'sum'),
            ENCOUNTER_COUNT=('ENCOUNTER_ID', 'nunique')
        )
        .assign(
            PMPM=lambda df: df['PAID_AMOUNT'] / member_count,
            ENCOUNTERS_PER_1000=lambda df: df['ENCOUNTER_COUNT'] * 12000.0 / member_count,
            PAID_PER_ENCOUNTER=lambda df: np.where(
                df['ENCOUNTER_COUNT'] == 0, 0.0, df['PAID_AMOUNT'] / df['ENCOUNTER_COUNT']
            )
        )
        [['ENCOUNTER_GROUP', 'ENCOUNTER_TYPE', 'PMPM', 'PAID_AMOUNT', 'ENCOUNTERS_PER_1000', 'PAID_PER_ENCOUNTER']]
    )

    # Add Grand Total row
    grand_total = {
        'ENCOUNTER_GROUP': 'Grand Total',
        'ENCOUNTER_TYPE': 'Grand Total',
        'PMPM': combined_df['PMPM'].sum(skipna=True),
        'ENCOUNTERS_PER_1000': combined_df['ENCOUNTERS_PER_1000'].sum(skipna=True),
        'PAID_PER_ENCOUNTER': combined_df['PAID_AMOUNT'].sum(skipna=True) / encounter_count if encounter_count else 0.0
    }

    result = pd.concat([combined_df, pd.DataFrame([grand_total])], ignore_index=True).dropna(subset=['ENCOUNTER_GROUP'])
    result = result.sort_values(by='PMPM', ascending=True, ignore_index=True)
    return result


# OUTLIERS BY Diagnosis #

@st.cache_data
def get_pmpm_by_diagnosis_category_csv(selected_year):
    """Get PMPM by diagnosis category for the selected year."""

    member_count = get_member_count(selected_year)
    df_by_year = outlier_claims_agg_data[outlier_claims_agg_data["INCR_YEAR"].eq(selected_year)]

    if member_count == 0 or df_by_year.empty:
        return pd.DataFrame(
            columns=[
                "DX_CCSR_CATEGORY2",
                "PMPM",
                "CUMULATIVE_PMPM",
                "PERCENT_OF_TOTAL_PMPM",
            ]
        )

    df_by_year["DX_CCSR_CATEGORY2"] = df_by_year["DX_CCSR_CATEGORY2"].fillna("null")
    pmpm_df = (
        df_by_year.groupby("DX_CCSR_CATEGORY2", as_index=False)["PAID_AMOUNT"]
        .sum()
        .assign(
            PMPM=lambda df: np.where(
                df["PAID_AMOUNT"] == 0, 0.0, df["PAID_AMOUNT"] / member_count 
            ),
            PERCENT_OF_TOTAL_PMPM=lambda df: (df["PMPM"] / df["PMPM"].sum()) * 100
        )
        .sort_values(by="PMPM", ascending=False, ignore_index=True)[
            ["DX_CCSR_CATEGORY2", "PMPM", "PERCENT_OF_TOTAL_PMPM"]
        ]
    )

    result = (
        pmpm_df.assign(CUMULATIVE_PMPM=lambda df: df["PMPM"].cumsum())
        .sort_values(by="PMPM", ascending=True, ignore_index=True)
        [
            ["DX_CCSR_CATEGORY2", "PMPM", "CUMULATIVE_PMPM", "PERCENT_OF_TOTAL_PMPM"]
        ])
    return result


@st.cache_data
def get_pmpm_by_diagnosis_csv(selected_year):
    """Get PMPM by diagnosis for the selected year."""
    member_count = get_member_count(selected_year)
    df_by_year = outlier_claims_agg_data[outlier_claims_agg_data["INCR_YEAR"].eq(selected_year)]

    if member_count == 0 or df_by_year.empty:
        return pd.DataFrame(
            columns=[
                "DX_DESCRIPTION",
                "PMPM",
                "CUMULATIVE_PMPM",
                "PERCENT_OF_TOTAL_PMPM",
            ]
        )

    df_by_year["DX_DESCRIPTION"] = df_by_year["DX_DESCRIPTION"].fillna("null")
    pmpm_df = (
        df_by_year.groupby("DX_DESCRIPTION", as_index=False)["PAID_AMOUNT"]
        .sum()
        .assign(
            PMPM=lambda df: np.where(
                df["PAID_AMOUNT"] == 0, 0.0, df["PAID_AMOUNT"] / member_count
            ),
            PERCENT_OF_TOTAL_PMPM=lambda df: (df["PMPM"] / df["PMPM"].sum()) * 100
        )
        .sort_values(by="PMPM", ascending=False, ignore_index=True)[
            ["DX_DESCRIPTION", "PMPM", "PERCENT_OF_TOTAL_PMPM"]
        ]
    )

    result = (
        pmpm_df.assign(CUMULATIVE_PMPM=lambda df: df["PMPM"].cumsum())
        .sort_values(by="PMPM", ascending=True, ignore_index=True)
        [
            ["DX_DESCRIPTION", "PMPM", "CUMULATIVE_PMPM", "PERCENT_OF_TOTAL_PMPM"]
        ])
    return result
