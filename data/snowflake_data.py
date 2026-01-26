"""
Data Access Layer for Delta Dental Project Planning Tracker
Provides functions to interact with Snowflake tables for Streamlit in Snowflake (SiS)
"""
import streamlit as st
import pandas as pd


def get_snowflake_session():
    """Get Snowflake session - works in both SiS and local development"""
    try:
        from snowflake.snowpark.context import get_active_session
        return get_active_session()
    except Exception:
        return None


def is_running_in_snowflake():
    """Check if app is running in Streamlit in Snowflake"""
    return get_snowflake_session() is not None


@st.cache_data(ttl=300)
def load_companies():
    """Load companies from Snowflake or fallback to sample data"""
    session = get_snowflake_session()
    if session:
        df = session.sql("""
            SELECT 
                COMPANY_ID, COMPANY_NAME, GROUP_AND_INDIVIDUAL_AFFILIATIONS,
                ABBREV, BRAND_COLOR, ONBOARDING_STATUS, ONBOARDING_PHASE,
                ONBOARDED_DATE, IS_CONTRACTED, CREATED_AT, UPDATED_AT
            FROM DDPA_PROJECT_TRACKER_DB.DATA.COMPANIES
            ORDER BY COMPANY_NAME
        """).to_pandas()
        return df
    else:
        from data.sample_data import sample_companies
        return sample_companies()


@st.cache_data(ttl=300)
def load_use_cases():
    """Load use cases from Snowflake or fallback to sample data"""
    session = get_snowflake_session()
    if session:
        df = session.sql("""
            SELECT 
                USE_CASE_ID, MEMBER_COMPANY_OR_AFFILIATION, TYPE, TITLE,
                DESCRIPTION, VALUE_OR_OUTCOME, KEY_DATA_DOMAINS, CURRENT_STATUS,
                ANTICIPATED_START_DATE, EST_TSHIRT_SIZE, EST_TIME, PARTNERS,
                CREATED_AT, UPDATED_AT
            FROM DDPA_PROJECT_TRACKER_DB.DATA.USE_CASES
            ORDER BY USE_CASE_ID
        """).to_pandas()
        return df
    else:
        from data.sample_data import sample_use_cases
        return sample_use_cases()


@st.cache_data(ttl=300)
def load_use_cases_with_company():
    """Load use cases with company info from Snowflake view"""
    session = get_snowflake_session()
    if session:
        df = session.sql("""
            SELECT * FROM DDPA_PROJECT_TRACKER_DB.DATA.V_USE_CASES_WITH_COMPANY
            ORDER BY USE_CASE_ID
        """).to_pandas()
        return df
    else:
        return load_use_cases()


@st.cache_data(ttl=300)
def load_contacts():
    """Load contacts from Snowflake or fallback to sample data"""
    session = get_snowflake_session()
    if session:
        df = session.sql("""
            SELECT * FROM DDPA_PROJECT_TRACKER_DB.DATA.V_CONTACTS_WITH_COMPANY
            ORDER BY NAME
        """).to_pandas()
        return df
    else:
        from data.sample_data import sample_contacts
        return sample_contacts()


@st.cache_data(ttl=300)
def load_meetings():
    """Load meetings from Snowflake or fallback to sample data"""
    session = get_snowflake_session()
    if session:
        df = session.sql("""
            SELECT * FROM DDPA_PROJECT_TRACKER_DB.DATA.MEETINGS
            ORDER BY MEETING_DATE DESC
        """).to_pandas()
        return df
    else:
        from data.sample_data import sample_meetings
        return sample_meetings()


@st.cache_data(ttl=300)
def load_monthly_spend():
    """Load monthly spend from Snowflake or fallback to sample data"""
    session = get_snowflake_session()
    if session:
        df = session.sql("""
            SELECT * FROM DDPA_PROJECT_TRACKER_DB.DATA.V_MONTHLY_SPEND_WITH_COMPANY
            ORDER BY MONTH_KEY
        """).to_pandas()
        return df
    else:
        from data.sample_data import sample_monthly_spend
        return sample_monthly_spend()


@st.cache_data(ttl=300)
def load_investments():
    """Load investments from Snowflake or fallback to sample data"""
    session = get_snowflake_session()
    if session:
        df = session.sql("""
            SELECT * FROM DDPA_PROJECT_TRACKER_DB.DATA.INVESTMENTS
            ORDER BY INVESTMENT_DATE DESC
        """).to_pandas()
        return df
    else:
        from data.sample_data import sample_investments
        return sample_investments()


@st.cache_data(ttl=300)
def load_marketplace_drawdowns():
    """Load marketplace drawdowns from Snowflake or fallback to sample data"""
    session = get_snowflake_session()
    if session:
        df = session.sql("""
            SELECT * FROM DDPA_PROJECT_TRACKER_DB.DATA.MARKETPLACE_DRAWDOWNS
            ORDER BY DRAWDOWN_DATE DESC
        """).to_pandas()
        return df
    else:
        from data.sample_data import sample_marketplace_drawdowns
        return sample_marketplace_drawdowns()


@st.cache_data(ttl=300)
def load_partners():
    """Load partners from Snowflake or fallback to sample data"""
    session = get_snowflake_session()
    if session:
        df = session.sql("""
            SELECT * FROM DDPA_PROJECT_TRACKER_DB.DATA.PARTNERS
            ORDER BY NAME
        """).to_pandas()
        return df
    else:
        from data.sample_data import sample_partners
        return sample_partners()


@st.cache_data(ttl=300)
def load_operating_areas():
    """Load member company operating areas from Snowflake"""
    session = get_snowflake_session()
    if session:
        df = session.sql("""
            SELECT * FROM DDPA_PROJECT_TRACKER_DB.DATA.MEMBER_COMPANY_OPERATING_AREAS
            ORDER BY OPERATING_AREAS
        """).to_pandas()
        return df
    else:
        from data.sample_data import sample_operating_areas
        return sample_operating_areas()


@st.cache_data(ttl=300)
def load_use_case_summary_by_status():
    """Load use case summary by status from Snowflake view"""
    session = get_snowflake_session()
    if session:
        df = session.sql("""
            SELECT * FROM DDPA_PROJECT_TRACKER_DB.DATA.V_USE_CASE_SUMMARY_BY_STATUS
        """).to_pandas()
        return df
    else:
        uc = load_use_cases()
        return uc.groupby('CURRENT_STATUS').size().reset_index(name='USE_CASE_COUNT')


@st.cache_data(ttl=300)
def load_use_case_summary_by_company():
    """Load use case summary by company from Snowflake view"""
    session = get_snowflake_session()
    if session:
        df = session.sql("""
            SELECT * FROM DDPA_PROJECT_TRACKER_DB.DATA.V_USE_CASE_SUMMARY_BY_COMPANY
        """).to_pandas()
        return df
    else:
        uc = load_use_cases()
        return uc.groupby('MEMBER_COMPANY_OR_AFFILIATION').size().reset_index(name='TOTAL_USE_CASES')


def save_use_case(use_case_data: dict):
    """Save a use case to Snowflake (insert or update)"""
    session = get_snowflake_session()
    if not session:
        st.warning("Cannot save to Snowflake - running in local mode")
        return False
    
    if use_case_data.get('USE_CASE_ID'):
        sql = f"""
            UPDATE DDPA_PROJECT_TRACKER_DB.DATA.USE_CASES
            SET MEMBER_COMPANY_OR_AFFILIATION = '{use_case_data.get('MEMBER_COMPANY_OR_AFFILIATION', '')}',
                TYPE = '{use_case_data.get('TYPE', '')}',
                TITLE = '{use_case_data.get('TITLE', '')}',
                DESCRIPTION = '{use_case_data.get('DESCRIPTION', '').replace("'", "''")}',
                VALUE_OR_OUTCOME = '{use_case_data.get('VALUE_OR_OUTCOME', '').replace("'", "''")}',
                KEY_DATA_DOMAINS = '{use_case_data.get('KEY_DATA_DOMAINS', '')}',
                CURRENT_STATUS = '{use_case_data.get('CURRENT_STATUS', '')}',
                ANTICIPATED_START_DATE = '{use_case_data.get('ANTICIPATED_START_DATE', '')}',
                EST_TSHIRT_SIZE = '{use_case_data.get('EST_TSHIRT_SIZE', '')}',
                EST_TIME = '{use_case_data.get('EST_TIME', '')}',
                PARTNERS = '{use_case_data.get('PARTNERS', '')}',
                UPDATED_AT = CURRENT_TIMESTAMP()
            WHERE USE_CASE_ID = {use_case_data['USE_CASE_ID']}
        """
    else:
        sql = f"""
            INSERT INTO DDPA_PROJECT_TRACKER_DB.DATA.USE_CASES
            (MEMBER_COMPANY_OR_AFFILIATION, TYPE, TITLE, DESCRIPTION, VALUE_OR_OUTCOME,
             KEY_DATA_DOMAINS, CURRENT_STATUS, ANTICIPATED_START_DATE, EST_TSHIRT_SIZE,
             EST_TIME, PARTNERS)
            VALUES (
                '{use_case_data.get('MEMBER_COMPANY_OR_AFFILIATION', '')}',
                '{use_case_data.get('TYPE', '')}',
                '{use_case_data.get('TITLE', '')}',
                '{use_case_data.get('DESCRIPTION', '').replace("'", "''")}',
                '{use_case_data.get('VALUE_OR_OUTCOME', '').replace("'", "''")}',
                '{use_case_data.get('KEY_DATA_DOMAINS', '')}',
                '{use_case_data.get('CURRENT_STATUS', '')}',
                '{use_case_data.get('ANTICIPATED_START_DATE', '')}',
                '{use_case_data.get('EST_TSHIRT_SIZE', '')}',
                '{use_case_data.get('EST_TIME', '')}',
                '{use_case_data.get('PARTNERS', '')}'
            )
        """
    
    try:
        session.sql(sql).collect()
        st.cache_data.clear()
        return True
    except Exception as e:
        st.error(f"Error saving use case: {e}")
        return False


def delete_use_case(use_case_id: int):
    """Delete a use case from Snowflake"""
    session = get_snowflake_session()
    if not session:
        st.warning("Cannot delete from Snowflake - running in local mode")
        return False
    
    try:
        session.sql(f"""
            DELETE FROM DDPA_PROJECT_TRACKER_DB.DATA.USE_CASES
            WHERE USE_CASE_ID = {use_case_id}
        """).collect()
        st.cache_data.clear()
        return True
    except Exception as e:
        st.error(f"Error deleting use case: {e}")
        return False


def save_contact(contact_data: dict):
    """Save a contact to Snowflake (insert or update)"""
    session = get_snowflake_session()
    if not session:
        st.warning("Cannot save to Snowflake - running in local mode")
        return False
    
    if contact_data.get('CONTACT_ID'):
        sql = f"""
            UPDATE DDPA_PROJECT_TRACKER_DB.DATA.CONTACTS
            SET NAME = '{contact_data.get('NAME', '')}',
                ROLE = '{contact_data.get('ROLE', '')}',
                COMPANY_ID = '{contact_data.get('COMPANY_ID', '')}',
                EMAIL = '{contact_data.get('EMAIL', '')}',
                PHONE = '{contact_data.get('PHONE', '')}',
                IS_PRIMARY = {contact_data.get('IS_PRIMARY', False)},
                UPDATED_AT = CURRENT_TIMESTAMP()
            WHERE CONTACT_ID = '{contact_data['CONTACT_ID']}'
        """
    else:
        import uuid
        contact_id = f"CT{str(uuid.uuid4())[:8].upper()}"
        sql = f"""
            INSERT INTO DDPA_PROJECT_TRACKER_DB.DATA.CONTACTS
            (CONTACT_ID, NAME, ROLE, COMPANY_ID, EMAIL, PHONE, IS_PRIMARY)
            VALUES (
                '{contact_id}',
                '{contact_data.get('NAME', '')}',
                '{contact_data.get('ROLE', '')}',
                '{contact_data.get('COMPANY_ID', '')}',
                '{contact_data.get('EMAIL', '')}',
                '{contact_data.get('PHONE', '')}',
                {contact_data.get('IS_PRIMARY', False)}
            )
        """
    
    try:
        session.sql(sql).collect()
        st.cache_data.clear()
        return True
    except Exception as e:
        st.error(f"Error saving contact: {e}")
        return False


def save_meeting(meeting_data: dict):
    """Save a meeting to Snowflake (insert or update)"""
    session = get_snowflake_session()
    if not session:
        st.warning("Cannot save to Snowflake - running in local mode")
        return False
    
    if meeting_data.get('MEETING_ID'):
        sql = f"""
            UPDATE DDPA_PROJECT_TRACKER_DB.DATA.MEETINGS
            SET MEETING_TYPE = '{meeting_data.get('MEETING_TYPE', '')}',
                GOVERNANCE_TIER = '{meeting_data.get('GOVERNANCE_TIER', '')}',
                MEETING_DATE = '{meeting_data.get('MEETING_DATE', '')}',
                STATUS = '{meeting_data.get('STATUS', '')}',
                ATTENDEES_EXPECTED = {meeting_data.get('ATTENDEES_EXPECTED', 0)},
                NOTES = '{meeting_data.get('NOTES', '').replace("'", "''")}',
                UPDATED_AT = CURRENT_TIMESTAMP()
            WHERE MEETING_ID = '{meeting_data['MEETING_ID']}'
        """
    else:
        import uuid
        meeting_id = f"MTG{str(uuid.uuid4())[:8].upper()}"
        sql = f"""
            INSERT INTO DDPA_PROJECT_TRACKER_DB.DATA.MEETINGS
            (MEETING_ID, MEETING_TYPE, GOVERNANCE_TIER, MEETING_DATE, STATUS, ATTENDEES_EXPECTED, NOTES)
            VALUES (
                '{meeting_id}',
                '{meeting_data.get('MEETING_TYPE', '')}',
                '{meeting_data.get('GOVERNANCE_TIER', '')}',
                '{meeting_data.get('MEETING_DATE', '')}',
                '{meeting_data.get('STATUS', '')}',
                {meeting_data.get('ATTENDEES_EXPECTED', 0)},
                '{meeting_data.get('NOTES', '').replace("'", "''")}'
            )
        """
    
    try:
        session.sql(sql).collect()
        st.cache_data.clear()
        return True
    except Exception as e:
        st.error(f"Error saving meeting: {e}")
        return False
