import streamlit as st
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

# Year list for dropdown selection
year_list = outlier_member_months_data['YEAR'].unique().tolist()

def get_metrics_data_csv(selected_year):
    """Get the number of member months for the selected year."""
    if selected_year:
        # Convert selected_year to string for comparison
        mask = outlier_member_months_data['YEAR'].astype(str) == str(selected_year)
        
        
        total_count = outlier_member_months_data[mask]['MEMBER_ID'].nunique()
        mean_age = outlier_member_months_data[mask]['AGE'].mean()
        female_count = outlier_member_months_data[mask & (outlier_member_months_data["SEX"] == 'female')]['MEMBER_ID'].nunique()
        
        return {
            "TOTAL_COUNT": total_count, 
            "MEAN_AGE": mean_age, 
            "FEMALE_COUNT": female_count
            }
    
    return {
        "TOTAL_COUNT": 0, 
        "MEAN_AGE": 0, 
        "FEMALE_COUNT": 0
        }


def get_outlier_claims_data_csv(selected_year):
    """Get the total paid amount and total encounters for the selected year."""
    mask = outlier_claims_agg_data['INCR_YEAR'].astype(str) == str(selected_year)
    
    total_paid = outlier_claims_agg_data[mask]['PAID_AMOUNT'].sum()
    total_encounters = outlier_claims_agg_data[mask]['ENCOUNTER_ID'].nunique()
    
    return {
        "TOTAL_PAID": total_paid, 
        "TOTAL_ENCOUNTERS": total_encounters
        }
    
    

def get_mean_paid_csv(selected_year):
    """Get the mean paid amount for the selected year."""
    mask = outlier_claims_agg_data['INCR_YEAR'].astype(str) == str(selected_year)
    return outlier_claims_agg_data[mask]['MEAN_PAID'].iloc[0] if not outlier_claims_agg_data[mask].empty else 0.0

def get_v24_risk_score_csv(selected_year):
    """Get the average HCC risk score for the selected year."""
    mask = outlier_member_months_data['YEAR'].astype(str) == str(selected_year)
    filtered_data = outlier_member_months_data[mask] if selected_year else pd.DataFrame()

    if not filtered_data.empty:
        v24_risk_mean = filtered_data['V24_RISK_SCORE'].mean()
        v24_risk_median = filtered_data['V24_RISK_SCORE'].median()
        v24_risk_min = filtered_data['V24_RISK_SCORE'].min()
        v24_risk_max = filtered_data['V24_RISK_SCORE'].max()
    else:
        v24_risk_mean = v24_risk_median = v24_risk_min = v24_risk_max = 0.0

    return {
        "V24_RISK_MEAN": v24_risk_mean,
        "V24_RISK_MEDIAN": v24_risk_median,
        "V24_RISK_MIN": v24_risk_min,
        "V24_RISK_MAX": v24_risk_max
    }

def get_outlier_population_by_race_csv(selected_year):
    """Get the outlier population by population for the selected year."""
    mask = outlier_member_months_data['YEAR'].astype(str) == str(selected_year)
    filtered_data = outlier_member_months_data[(mask) & (outlier_member_months_data["RACE"].notnull())] if selected_year else pd.DataFrame()
    if not filtered_data.empty:
        population_by_race = filtered_data.groupby('RACE')['MEMBER_ID'].nunique().reset_index(name='MEMBER_COUNT')
        total_members = population_by_race['MEMBER_COUNT'].sum()
        population_by_race['PERCENTAGE'] = (population_by_race['MEMBER_COUNT'] / total_members * 100).round(2)
        population_by_race = population_by_race.sort_values('PERCENTAGE')
        
    return population_by_race

def get_outlier_population_by_state_csv(selected_year):
    """Get the outlier population by population for the selected year."""
    mask = outlier_member_months_data['YEAR'].astype(str) == str(selected_year)
    filtered_data = outlier_member_months_data[(mask) & (outlier_member_months_data["STATE"].notnull())] if selected_year else pd.DataFrame()
    if not filtered_data.empty:
        population_by_state = filtered_data.groupby('STATE')['MEMBER_ID'].nunique().reset_index(name='MEMBER_COUNT')
        total_members = population_by_state['MEMBER_COUNT'].sum()
        population_by_state['PERCENTAGE'] = (population_by_state['MEMBER_COUNT'] / total_members * 100).round(2)
        population_by_state = population_by_state.sort_values('PERCENTAGE')
        
    return population_by_state