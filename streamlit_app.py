"""
Delta Dental Project Planning Tracker
A collaborative framework for tracking use cases and roadmaps across member companies.
Co-branded solution by DDPA and Snowflake.

Deployed to Streamlit in Snowflake (SiS) - pulls all data from Snowflake tables.
Single-file application with all functionality inlined.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import io
import base64
from pathlib import Path

DELTA_DENTAL_GREEN = "#39B54A"
SNOWFLAKE_BLUE = "#29B5E8"

STATUSES = ["Not Started", "Discovery", "In Progress", "On Hold", "Completed", "Cancelled"]
CATEGORIES = [
    "Data Analytics & BI", "Machine Learning & AI", "Data Sharing & Collaboration",
    "Claims Processing", "Member Experience", "Provider Network", "Fraud Detection",
    "Regulatory Compliance", "Data Platform & Infrastructure", "Cost Optimization"
]
GOVERNANCE_TIERS = {
    "operations_work_group": {
        "name": "Umbrella Deal Operations Work Group",
        "description": "Monitor Snowflake spend, provide direction on investment spend, and general oversight",
        "cadence": "Monthly (moving to Quarterly)",
    },
    "steering_committee": {
        "name": "Snowflake Steering Committee", 
        "description": "Provide strategic oversight and guidance to all member companies leveraging Snowflake",
        "cadence": "Monthly",
    },
    "user_community": {
        "name": "Snowflake User Community",
        "description": "Ongoing education, hands-on labs, workshops aligned to member company priorities",
        "cadence": "Monthly/Bi-Monthly",
    }
}


def get_snowflake_session():
    from snowflake.snowpark.context import get_active_session
    return get_active_session()


@st.cache_data(ttl=300)
def load_companies():
    session = get_snowflake_session()
    return session.sql("""
        SELECT 
            COMPANY_ID, COMPANY_NAME, GROUP_AND_INDIVIDUAL_AFFILIATIONS,
            ABBREV, BRAND_COLOR, ONBOARDING_STATUS, ONBOARDING_PHASE,
            ONBOARDED_DATE, IS_CONTRACTED, CREATED_AT, UPDATED_AT
        FROM DDPA_PROJECT_TRACKER_DB.DATA.COMPANIES
        ORDER BY COMPANY_NAME
    """).to_pandas()


@st.cache_data(ttl=300)
def load_use_cases():
    session = get_snowflake_session()
    return session.sql("""
        SELECT 
            USE_CASE_ID, MEMBER_COMPANY_OR_AFFILIATION, TYPE, TITLE,
            DESCRIPTION, VALUE_OR_OUTCOME, KEY_DATA_DOMAINS, CURRENT_STATUS,
            ANTICIPATED_START_DATE, EST_TSHIRT_SIZE, EST_TIME, PARTNERS,
            CREATED_AT, UPDATED_AT
        FROM DDPA_PROJECT_TRACKER_DB.DATA.USE_CASES
        ORDER BY USE_CASE_ID
    """).to_pandas()


@st.cache_data(ttl=300)
def load_use_cases_with_company():
    session = get_snowflake_session()
    return session.sql("""
        SELECT * FROM DDPA_PROJECT_TRACKER_DB.DATA.V_USE_CASES_WITH_COMPANY
        ORDER BY USE_CASE_ID
    """).to_pandas()


@st.cache_data(ttl=300)
def load_contacts():
    session = get_snowflake_session()
    return session.sql("""
        SELECT * FROM DDPA_PROJECT_TRACKER_DB.DATA.V_CONTACTS_WITH_COMPANY
        ORDER BY NAME
    """).to_pandas()


@st.cache_data(ttl=300)
def load_meetings():
    session = get_snowflake_session()
    return session.sql("""
        SELECT * FROM DDPA_PROJECT_TRACKER_DB.DATA.MEETINGS
        ORDER BY MEETING_DATE DESC
    """).to_pandas()


@st.cache_data(ttl=300)
def load_monthly_spend():
    session = get_snowflake_session()
    return session.sql("""
        SELECT * FROM DDPA_PROJECT_TRACKER_DB.DATA.V_MONTHLY_SPEND_WITH_COMPANY
        ORDER BY MONTH_KEY
    """).to_pandas()


@st.cache_data(ttl=300)
def load_investments():
    session = get_snowflake_session()
    return session.sql("""
        SELECT * FROM DDPA_PROJECT_TRACKER_DB.DATA.INVESTMENTS
        ORDER BY INVESTMENT_DATE DESC
    """).to_pandas()


@st.cache_data(ttl=300)
def load_marketplace_drawdowns():
    session = get_snowflake_session()
    return session.sql("""
        SELECT * FROM DDPA_PROJECT_TRACKER_DB.DATA.MARKETPLACE_DRAWDOWNS
        ORDER BY DRAWDOWN_DATE DESC
    """).to_pandas()


@st.cache_data(ttl=300)
def load_partners():
    session = get_snowflake_session()
    return session.sql("""
        SELECT * FROM DDPA_PROJECT_TRACKER_DB.DATA.PARTNERS
        ORDER BY NAME
    """).to_pandas()


@st.cache_data(ttl=300)
def load_operating_areas():
    session = get_snowflake_session()
    return session.sql("""
        SELECT * FROM DDPA_PROJECT_TRACKER_DB.DATA.MEMBER_COMPANY_OPERATING_AREAS
        ORDER BY OPERATING_AREAS
    """).to_pandas()


@st.cache_data(ttl=300)
def load_use_case_summary_by_status():
    session = get_snowflake_session()
    return session.sql("""
        SELECT * FROM DDPA_PROJECT_TRACKER_DB.DATA.V_USE_CASE_SUMMARY_BY_STATUS
    """).to_pandas()


@st.cache_data(ttl=300)
def load_use_case_summary_by_company():
    session = get_snowflake_session()
    return session.sql("""
        SELECT * FROM DDPA_PROJECT_TRACKER_DB.DATA.V_USE_CASE_SUMMARY_BY_COMPANY
    """).to_pandas()


def save_use_case(use_case_data: dict):
    session = get_snowflake_session()
    
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
    session = get_snowflake_session()
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
    session = get_snowflake_session()
    
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
    session = get_snowflake_session()
    
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


def get_company_name(company_id: str) -> str:
    companies = load_companies()
    match = companies[companies['COMPANY_ID'] == company_id]
    if len(match) > 0:
        return match['COMPANY_NAME'].iloc[0]
    return company_id


def get_company_color(company_id: str) -> str:
    companies = load_companies()
    match = companies[companies['COMPANY_ID'] == company_id]
    if len(match) > 0:
        return match['BRAND_COLOR'].iloc[0]
    return "#666666"


def export_to_excel(df):
    try:
        export_df = df.copy()
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            export_df.to_excel(writer, sheet_name='Use Cases', index=False)
            worksheet = writer.sheets['Use Cases']
            for idx, col in enumerate(export_df.columns):
                max_length = max(export_df[col].astype(str).map(len).max(), len(col)) + 2
                worksheet.column_dimensions[chr(65 + idx)].width = min(max_length, 50)
        output.seek(0)
        return output.getvalue()
    except Exception:
        output = io.StringIO()
        df.to_csv(output, index=False)
        return output.getvalue().encode('utf-8')


st.set_page_config(
    page_title="Delta Dental Project Tracker | DDPA × Snowflake",
    page_icon="🦷",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');
    :root {
        --delta-green: #39B54A;
        --delta-green-dark: #2D9340;
        --snowflake-blue: #29B5E8;
    }
    .stApp { font-family: 'Plus Jakarta Sans', sans-serif; }
    .main-header {
        background: linear-gradient(135deg, #39B54A 0%, #2D9340 40%, #29B5E8 100%);
        padding: 1.5rem 2rem; border-radius: 16px; margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(57, 181, 74, 0.25);
    }
    .main-header h1 { color: white; font-weight: 700; font-size: 1.75rem; margin: 0; }
    .main-header p { color: rgba(255, 255, 255, 0.95); font-size: 0.95rem; margin: 0.25rem 0 0 0; }
    .co-brand {
        display: inline-flex; align-items: center; gap: 0.75rem;
        background: rgba(255, 255, 255, 0.2); padding: 0.5rem 1rem;
        border-radius: 50px; font-size: 0.85rem; color: white; margin-top: 0.75rem;
    }
    .metric-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
        border: 1px solid #e2e8f0; border-radius: 16px; padding: 1.5rem;
        text-align: center; box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
    }
    .metric-card:hover { transform: translateY(-4px); box-shadow: 0 12px 32px rgba(57, 181, 74, 0.12); border-color: #39B54A; }
    .metric-value { font-size: 2.5rem; font-weight: 700; color: #39B54A; line-height: 1; }
    .metric-label { font-size: 0.9rem; color: #64748b; margin-top: 0.5rem; font-weight: 500; }
    .status-pill { display: inline-block; padding: 0.35rem 0.9rem; border-radius: 50px; font-size: 0.8rem; font-weight: 600; }
    .status-in-progress { background: #dbeafe; color: #1d4ed8; }
    .status-completed { background: #dcfce7; color: #166534; }
    .status-discovery { background: #fef3c7; color: #92400e; }
    .status-not-started { background: #f1f5f9; color: #475569; }
    .use-case-card { background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.25rem; margin-bottom: 1rem; }
    .use-case-card:hover { border-color: #39B54A; box-shadow: 0 8px 24px rgba(57, 181, 74, 0.15); }
    .progress-container { background: #e2e8f0; border-radius: 50px; height: 8px; overflow: hidden; }
    .progress-bar { height: 100%; border-radius: 50px; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

if 'use_cases' not in st.session_state:
    st.session_state.use_cases = load_use_cases()
if 'contacts' not in st.session_state:
    st.session_state.contacts = load_contacts()
if 'meetings' not in st.session_state:
    st.session_state.meetings = load_meetings()
if 'companies' not in st.session_state:
    st.session_state.companies = load_companies()
if 'selected_view' not in st.session_state:
    st.session_state.selected_view = "Dashboard"


def get_app_root():
    return Path(__file__).parent


def get_logo_base64(logo_name="delta-dental-logo.webp"):
    app_root = get_app_root()
    logo_path = app_root / "assets" / logo_name
    if not logo_path.exists():
        logo_path = app_root / logo_name
    if logo_path.exists():
        with open(logo_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None


def get_snowflake_icon_base64():
    app_root = get_app_root()
    icon_path = app_root / "SNOW-ICON.png"
    if icon_path.exists():
        with open(icon_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None


def render_header():
    dd_logo_base64 = get_logo_base64()
    snow_icon_base64 = get_snowflake_icon_base64()
    
    dd_logo_html = f'<img src="data:image/webp;base64,{dd_logo_base64}" alt="Delta Dental" style="width:60px;height:60px;object-fit:contain;background:white;border-radius:8px;padding:4px;">' if dd_logo_base64 else '🦷'
    snow_icon_html = f'<img src="data:image/png;base64,{snow_icon_base64}" alt="Snowflake" style="height: 24px;">' if snow_icon_base64 else '❄️'
    
    st.markdown(f"""
    <div class="main-header">
        <div style="display: flex; align-items: center; gap: 1.5rem;">
            <div>{dd_logo_html}</div>
            <div>
                <h1>Delta Dental Project Planning Tracker</h1>
                <p>Collaborative Use Case & Roadmap Management Across Member Companies</p>
                <div class="co-brand">
                    <span style="font-weight: 600;">DDPA</span>
                    <span style="width:1px;height:16px;background:rgba(255,255,255,0.5);"></span>
                    <span style="display: flex; align-items: center; gap: 6px;">{snow_icon_html} Snowflake Partnership</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_sidebar():
    with st.sidebar:
        st.markdown("### 🧭 Navigation")
        
        view_options = [
            "📊 Dashboard", "🏛️ Governance", "💰 Financial Tracking", "📋 Use Cases",
            "🗺️ Roadmap", "🏢 Member Companies", "👥 Contacts", "📅 Meetings", "⚙️ Settings"
        ]
        
        selected = st.radio("Select View", view_options, label_visibility="collapsed")
        st.session_state.selected_view = selected.split(" ", 1)[1]
        
        st.markdown("---")
        st.markdown("### 🎯 Filters")
        
        companies = st.session_state.companies
        company_options = ["All Companies"] + companies['COMPANY_NAME'].tolist()
        selected_company = st.selectbox("Member Company", company_options)
        
        status_options = ["All Statuses"] + STATUSES
        selected_status = st.selectbox("Status", status_options)
        
        category_options = ["All Categories"] + CATEGORIES
        selected_category = st.selectbox("Category", category_options)
        
        st.markdown("---")
        st.markdown("### 📈 Quick Stats")
        df = st.session_state.use_cases
        
        col1, col2 = st.columns(2)
        with col1:
            active = len(df[df['CURRENT_STATUS'] == 'In Progress']) if 'CURRENT_STATUS' in df.columns else 0
            st.metric("Active", active)
        with col2:
            st.metric("Total", len(df))
        
        if st.button("🔄 Refresh Data"):
            st.cache_data.clear()
            st.session_state.use_cases = load_use_cases()
            st.session_state.contacts = load_contacts()
            st.session_state.meetings = load_meetings()
            st.session_state.companies = load_companies()
            st.rerun()
        
        return {
            'company': None if selected_company == "All Companies" else selected_company,
            'status': None if selected_status == "All Statuses" else selected_status,
            'category': None if selected_category == "All Categories" else selected_category
        }


def filter_use_cases(df, filters):
    filtered_df = df.copy()
    
    if filters['company']:
        companies = st.session_state.companies
        match = companies[companies['COMPANY_NAME'] == filters['company']]
        if len(match) > 0:
            company_id = match['COMPANY_ID'].iloc[0]
            filtered_df = filtered_df[filtered_df['MEMBER_COMPANY_OR_AFFILIATION'] == company_id]
    
    if filters['status'] and 'CURRENT_STATUS' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['CURRENT_STATUS'] == filters['status']]
    
    if filters['category'] and 'KEY_DATA_DOMAINS' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['KEY_DATA_DOMAINS'] == filters['category']]
    
    return filtered_df


def render_dashboard(filters):
    df = filter_use_cases(st.session_state.use_cases, filters)
    companies = st.session_state.companies
    
    st.markdown("### 📊 Key Metrics")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{len(df)}</div><div class="metric-label">Total Use Cases</div></div>', unsafe_allow_html=True)
    
    with col2:
        in_progress = len(df[df['CURRENT_STATUS'] == 'In Progress']) if 'CURRENT_STATUS' in df.columns else 0
        st.markdown(f'<div class="metric-card"><div class="metric-value" style="color: #1d4ed8;">{in_progress}</div><div class="metric-label">In Progress</div></div>', unsafe_allow_html=True)
    
    with col3:
        discovery = len(df[df['CURRENT_STATUS'] == 'Discovery']) if 'CURRENT_STATUS' in df.columns else 0
        st.markdown(f'<div class="metric-card"><div class="metric-value" style="color: #f59e0b;">{discovery}</div><div class="metric-label">Discovery</div></div>', unsafe_allow_html=True)
    
    with col4:
        completed = len(df[df['CURRENT_STATUS'] == 'Completed']) if 'CURRENT_STATUS' in df.columns else 0
        st.markdown(f'<div class="metric-card"><div class="metric-value" style="color: #16a34a;">{completed}</div><div class="metric-label">Completed</div></div>', unsafe_allow_html=True)
    
    with col5:
        companies_active = df['MEMBER_COMPANY_OR_AFFILIATION'].nunique() if 'MEMBER_COMPANY_OR_AFFILIATION' in df.columns else 0
        st.markdown(f'<div class="metric-card"><div class="metric-value" style="color: #7c3aed;">{companies_active}</div><div class="metric-label">Companies Active</div></div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Status Distribution")
        if 'CURRENT_STATUS' in df.columns and len(df) > 0:
            status_counts = df['CURRENT_STATUS'].value_counts().reset_index()
            status_counts.columns = ['Status', 'Count']
            fig = px.pie(status_counts, values='Count', names='Status', hole=0.4,
                        color='Status', color_discrete_map={
                            'In Progress': '#3b82f6', 'Completed': '#22c55e', 'Discovery': '#f59e0b',
                            'Not Started': '#94a3b8', 'On Hold': '#ef4444', 'Cancelled': '#6b7280'
                        })
            fig.update_layout(showlegend=True, legend=dict(orientation="h", y=-0.2), margin=dict(t=20, b=80, l=20, r=20), height=300)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No status data available")
    
    with col2:
        st.markdown("#### Use Cases by Category")
        if 'KEY_DATA_DOMAINS' in df.columns and len(df) > 0:
            category_counts = df['KEY_DATA_DOMAINS'].value_counts().reset_index()
            category_counts.columns = ['Category', 'Count']
            fig = px.bar(category_counts, x='Count', y='Category', orientation='h', color='Count', color_continuous_scale='Blues')
            fig.update_layout(showlegend=False, margin=dict(t=20, b=20, l=20, r=20), height=300, yaxis={'categoryorder': 'total ascending'})
            fig.update_coloraxes(showscale=False)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No category data available")
    
    st.markdown("#### 🏢 Activity by Member Company")
    if 'MEMBER_COMPANY_OR_AFFILIATION' in df.columns and len(df) > 0:
        company_counts = df['MEMBER_COMPANY_OR_AFFILIATION'].value_counts().reset_index()
        company_counts.columns = ['COMPANY_ID', 'Count']
        company_counts = company_counts.merge(companies[['COMPANY_ID', 'COMPANY_NAME', 'ABBREV']], on='COMPANY_ID', how='left')
        company_counts['Display'] = company_counts['ABBREV'].fillna(company_counts['COMPANY_ID'])
        
        fig = px.bar(company_counts, x='Display', y='Count', color='Count', color_continuous_scale='Blues')
        fig.update_layout(xaxis_title="Company", yaxis_title="Use Cases", margin=dict(t=20, b=20, l=20, r=20), height=300)
        fig.update_coloraxes(showscale=False)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("#### 📋 Recent Use Cases")
    recent = df.head(5)
    for _, row in recent.iterrows():
        title = row.get('TITLE', 'Untitled')
        status = row.get('CURRENT_STATUS', 'Unknown')
        company = get_company_name(row.get('MEMBER_COMPANY_OR_AFFILIATION', ''))
        status_class = f"status-{status.lower().replace(' ', '-')}" if status else ""
        st.markdown(f"""
        <div class="use-case-card">
            <strong>{title}</strong>
            <div style="font-size: 0.85rem; color: #64748b; margin-top: 0.25rem;">
                {company} | <span class="status-pill {status_class}">{status}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_use_cases(filters):
    df = filter_use_cases(st.session_state.use_cases, filters)
    companies = st.session_state.companies
    
    st.markdown("### 📋 Use Cases Management")
    
    tab1, tab2 = st.tabs(["📋 View All", "➕ Add New"])
    
    with tab1:
        col1, col2 = st.columns([1, 4])
        with col1:
            view_type = st.selectbox("View", ["Table", "Cards"], label_visibility="collapsed")
        with col2:
            if len(df) > 0:
                st.download_button("📥 Export Excel", export_to_excel(df), file_name="use_cases_export.xlsx",
                                  mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        
        if view_type == "Table":
            display_cols = ['USE_CASE_ID', 'TITLE', 'MEMBER_COMPANY_OR_AFFILIATION', 'KEY_DATA_DOMAINS', 'CURRENT_STATUS']
            display_cols = [c for c in display_cols if c in df.columns]
            if display_cols:
                st.dataframe(df[display_cols], use_container_width=True, hide_index=True)
            else:
                st.info("No data to display")
        else:
            for _, row in df.iterrows():
                title = row.get('TITLE', 'Untitled')
                desc = row.get('DESCRIPTION', '')[:150] + '...' if row.get('DESCRIPTION') and len(str(row.get('DESCRIPTION'))) > 150 else row.get('DESCRIPTION', '')
                status = row.get('CURRENT_STATUS', 'Unknown')
                company = get_company_name(row.get('MEMBER_COMPANY_OR_AFFILIATION', ''))
                
                st.markdown(f"""
                <div class="use-case-card">
                    <strong>{row.get('USE_CASE_ID', '')} | {title}</strong>
                    <div style="font-size: 0.85rem; color: #64748b; margin: 0.5rem 0;">{desc}</div>
                    <div>
                        <span class="status-pill status-{status.lower().replace(' ', '-')}">{status}</span>
                        <span style="margin-left: 1rem; color: #64748b;">Lead: {company}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("#### ➕ Add New Use Case")
        
        with st.form("add_use_case"):
            col1, col2 = st.columns(2)
            with col1:
                title = st.text_input("Title*")
                category = st.selectbox("Category*", CATEGORIES)
                company_names = companies['COMPANY_NAME'].tolist()
                lead_company_name = st.selectbox("Lead Company*", company_names)
            with col2:
                description = st.text_area("Description")
                status = st.selectbox("Status", STATUSES)
                start_date = st.date_input("Anticipated Start Date")
            
            value_outcome = st.text_input("Value/Outcome", placeholder="e.g., $1.5M savings")
            
            submitted = st.form_submit_button("➕ Create Use Case", type="primary", use_container_width=True)
            
            if submitted and title:
                company_match = companies[companies['COMPANY_NAME'] == lead_company_name]
                company_id = company_match['COMPANY_ID'].iloc[0] if len(company_match) > 0 else ''
                
                use_case_data = {
                    'MEMBER_COMPANY_OR_AFFILIATION': company_id,
                    'TYPE': 'Use Case',
                    'TITLE': title,
                    'DESCRIPTION': description,
                    'VALUE_OR_OUTCOME': value_outcome,
                    'KEY_DATA_DOMAINS': category,
                    'CURRENT_STATUS': status,
                    'ANTICIPATED_START_DATE': start_date.strftime("%Y-%m-%d"),
                }
                
                if save_use_case(use_case_data):
                    st.success(f"✅ Use case '{title}' created!")
                    st.session_state.use_cases = load_use_cases()
                    st.rerun()


def render_roadmap(filters):
    df = filter_use_cases(st.session_state.use_cases, filters)
    
    st.markdown("### 🗺️ Master Roadmap")
    
    if 'ANTICIPATED_START_DATE' in df.columns and len(df) > 0:
        df_with_dates = df[df['ANTICIPATED_START_DATE'].notna()].copy()
        
        if len(df_with_dates) > 0:
            df_with_dates['START'] = pd.to_datetime(df_with_dates['ANTICIPATED_START_DATE'])
            df_with_dates['END'] = df_with_dates['START'] + pd.Timedelta(days=90)
            df_with_dates['TASK'] = df_with_dates['USE_CASE_ID'].astype(str) + ': ' + df_with_dates['TITLE'].str[:30]
            
            fig = px.timeline(df_with_dates, x_start='START', x_end='END', y='TASK', color='CURRENT_STATUS',
                            color_discrete_map={'In Progress': '#3b82f6', 'Completed': '#22c55e', 
                                               'Discovery': '#f59e0b', 'Not Started': '#94a3b8'})
            fig.update_layout(height=max(400, len(df_with_dates) * 40), xaxis_title="Timeline", yaxis_title="")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No use cases with start dates to display on roadmap")
    else:
        st.info("Start date information not available for roadmap view")


def render_member_companies():
    st.markdown("### 🏢 Member Companies")
    
    companies = st.session_state.companies
    use_cases = st.session_state.use_cases
    contacts = st.session_state.contacts
    
    if len(companies) == 0:
        st.warning("No company data available")
        return
    
    tabs = st.tabs(companies['ABBREV'].fillna(companies['COMPANY_ID']).tolist())
    
    for i, tab in enumerate(tabs):
        with tab:
            company = companies.iloc[i]
            company_id = company['COMPANY_ID']
            color = company.get('BRAND_COLOR', '#0066B1')
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, {color}15, {color}05); 
                        border-left: 4px solid {color}; padding: 1.5rem; border-radius: 12px; margin-bottom: 1.5rem;">
                <h2 style="margin: 0; color: {color};">{company['COMPANY_NAME']}</h2>
                <div style="color: #64748b; margin-top: 0.5rem;">
                    Status: {company.get('ONBOARDING_STATUS', 'N/A')} | Phase: {company.get('ONBOARDING_PHASE', 'N/A')}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            company_uc = use_cases[use_cases['MEMBER_COMPANY_OR_AFFILIATION'] == company_id] if 'MEMBER_COMPANY_OR_AFFILIATION' in use_cases.columns else pd.DataFrame()
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Use Cases", len(company_uc))
            col2.metric("In Progress", len(company_uc[company_uc['CURRENT_STATUS'] == 'In Progress']) if 'CURRENT_STATUS' in company_uc.columns else 0)
            col3.metric("Completed", len(company_uc[company_uc['CURRENT_STATUS'] == 'Completed']) if 'CURRENT_STATUS' in company_uc.columns else 0)
            
            if 'COMPANY_ID' in contacts.columns:
                company_contacts = contacts[contacts['COMPANY_ID'] == company_id]
                if len(company_contacts) > 0:
                    st.markdown("##### 👥 Key Contacts")
                    for _, contact in company_contacts.iterrows():
                        primary = "🌟 " if contact.get('IS_PRIMARY') else ""
                        st.markdown(f"**{primary}{contact.get('NAME', '')}** - {contact.get('ROLE', '')}  \n📧 {contact.get('EMAIL', '')}")


def render_contacts():
    st.markdown("### 👥 Contacts")
    
    contacts = st.session_state.contacts
    
    if len(contacts) == 0:
        st.warning("No contacts available")
        return
    
    tab1, tab2 = st.tabs(["📇 View Contacts", "➕ Add Contact"])
    
    with tab1:
        display_cols = ['NAME', 'ROLE', 'COMPANY_NAME', 'EMAIL', 'IS_PRIMARY']
        display_cols = [c for c in display_cols if c in contacts.columns]
        if display_cols:
            st.dataframe(contacts[display_cols], use_container_width=True, hide_index=True)
    
    with tab2:
        with st.form("add_contact"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Name*")
                role = st.text_input("Role")
                email = st.text_input("Email")
            with col2:
                companies = st.session_state.companies
                company_name = st.selectbox("Company", companies['COMPANY_NAME'].tolist())
                phone = st.text_input("Phone")
                is_primary = st.checkbox("Primary Contact")
            
            if st.form_submit_button("➕ Add Contact", type="primary"):
                company_match = companies[companies['COMPANY_NAME'] == company_name]
                company_id = company_match['COMPANY_ID'].iloc[0] if len(company_match) > 0 else ''
                
                contact_data = {
                    'NAME': name, 'ROLE': role, 'COMPANY_ID': company_id,
                    'EMAIL': email, 'PHONE': phone, 'IS_PRIMARY': is_primary
                }
                if save_contact(contact_data):
                    st.success(f"✅ Contact '{name}' added!")
                    st.session_state.contacts = load_contacts()
                    st.rerun()


def render_meetings():
    st.markdown("### 📅 Meetings")
    
    meetings = st.session_state.meetings
    
    if len(meetings) == 0:
        st.warning("No meetings available")
        return
    
    st.markdown("#### 📆 Upcoming Meetings")
    
    today = datetime.now().strftime("%Y-%m-%d")
    date_col = 'MEETING_DATE' if 'MEETING_DATE' in meetings.columns else None
    
    if date_col:
        upcoming = meetings[meetings[date_col] >= today].head(5)
        for _, meeting in upcoming.iterrows():
            meeting_type = meeting.get('MEETING_TYPE', '')
            tier_color = "#dc2626" if "Operations" in str(meeting_type) else "#0066B1" if "Steering" in str(meeting_type) else "#16a34a"
            
            st.markdown(f"""
            <div style="background: white; border-left: 4px solid {tier_color}; border-radius: 0 8px 8px 0; padding: 1rem; margin-bottom: 0.5rem;">
                <div style="display: flex; justify-content: space-between;">
                    <strong>{meeting_type}</strong>
                    <span style="background: #f1f5f9; padding: 0.25rem 0.75rem; border-radius: 4px;">{meeting.get(date_col, '')}</span>
                </div>
                <div style="font-size: 0.85rem; color: #64748b; margin-top: 0.5rem;">{meeting.get('NOTES', '')}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    display_cols = ['MEETING_TYPE', 'MEETING_DATE', 'STATUS', 'NOTES']
    display_cols = [c for c in display_cols if c in meetings.columns]
    if display_cols:
        st.dataframe(meetings[display_cols], use_container_width=True, hide_index=True)


def render_governance():
    st.markdown("### 🏛️ Governance Structure")
    
    col1, col2, col3 = st.columns(3)
    
    for i, (tier_key, tier) in enumerate(GOVERNANCE_TIERS.items()):
        with [col1, col2, col3][i]:
            color = "#dc2626" if "operations" in tier_key else "#0066B1" if "steering" in tier_key else "#16a34a"
            st.markdown(f"""
            <div class="metric-card" style="border-left: 4px solid {color};">
                <div class="metric-value" style="font-size: 1.2rem; color: {color};">{tier['name'].split()[0]}</div>
                <div class="metric-label">{tier['cadence']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    for tier_key, tier in GOVERNANCE_TIERS.items():
        with st.expander(f"**{tier['name']}**", expanded=False):
            st.markdown(f"**Description:** {tier['description']}")
            st.markdown(f"**Cadence:** {tier['cadence']}")


def render_financial_tracking():
    st.markdown("### 💰 Financial Tracking")
    
    try:
        spend_df = load_monthly_spend()
        investments_df = load_investments()
        drawdowns_df = load_marketplace_drawdowns()
        
        tab1, tab2, tab3 = st.tabs(["📈 Spend Overview", "💵 Investments", "🏪 Drawdowns"])
        
        with tab1:
            if len(spend_df) > 0:
                st.dataframe(spend_df, use_container_width=True, hide_index=True)
            else:
                st.info("No spend data available")
        
        with tab2:
            if len(investments_df) > 0:
                st.dataframe(investments_df, use_container_width=True, hide_index=True)
            else:
                st.info("No investment data available")
        
        with tab3:
            if len(drawdowns_df) > 0:
                st.dataframe(drawdowns_df, use_container_width=True, hide_index=True)
            else:
                st.info("No drawdown data available")
    
    except Exception as e:
        st.error(f"Error loading financial data: {e}")


def render_settings():
    st.markdown("### ⚙️ Settings")
    
    tab1, tab2 = st.tabs(["🔗 Data Connection", "📊 Data Management"])
    
    with tab1:
        st.markdown("#### Snowflake Connection")
        st.info("This app is connected to Snowflake and pulling live data from DDPA_PROJECT_TRACKER_DB")
        
        st.markdown("**Connected Tables:**")
        st.markdown("""
        - `DATA.COMPANIES` - Member companies
        - `DATA.USE_CASES` - Use case tracking
        - `DATA.CONTACTS` - Contact information
        - `DATA.MEETINGS` - Meeting schedule
        - `DATA.MONTHLY_SPEND` - Financial tracking
        - `DATA.INVESTMENTS` - Investment allocations
        - `DATA.MARKETPLACE_DRAWDOWNS` - Marketplace usage
        """)
    
    with tab2:
        st.markdown("#### Data Management")
        
        if st.button("🔄 Refresh All Data", use_container_width=True):
            st.cache_data.clear()
            st.session_state.use_cases = load_use_cases()
            st.session_state.contacts = load_contacts()
            st.session_state.meetings = load_meetings()
            st.session_state.companies = load_companies()
            st.success("✅ Data refreshed from Snowflake!")
            st.rerun()


def render_footer():
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; color: #64748b; font-size: 0.85rem;">
        © {datetime.now().year} DDPA × Snowflake Partnership | Project Planning Tracker | Live Data from Snowflake
    </div>
    """, unsafe_allow_html=True)


def main():
    render_header()
    filters = render_sidebar()
    
    view = st.session_state.selected_view
    
    if view == "Dashboard":
        render_dashboard(filters)
    elif view == "Governance":
        render_governance()
    elif view == "Financial Tracking":
        render_financial_tracking()
    elif view == "Use Cases":
        render_use_cases(filters)
    elif view == "Roadmap":
        render_roadmap(filters)
    elif view == "Member Companies":
        render_member_companies()
    elif view == "Contacts":
        render_contacts()
    elif view == "Meetings":
        render_meetings()
    elif view == "Settings":
        render_settings()
    
    render_footer()


if __name__ == "__main__":
    main()
