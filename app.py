"""
Delta Dental Project Planning Tracker
A collaborative framework for tracking use cases and roadmaps across member companies.
Co-branded solution by DDPA and Snowflake.

Supports deployment to:
- Local Streamlit
- Streamlit in Snowflake (Container Runtime)
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import base64
from pathlib import Path
import os

# Brand colors
DELTA_DENTAL_GREEN = "#39B54A"
SNOWFLAKE_BLUE = "#29B5E8"

# Detect if running in Snowflake
IS_RUNNING_IN_SNOWFLAKE = os.environ.get("SNOWFLAKE_ENVIRONMENT") is not None


def get_app_root():
    """Get the root directory of the app, compatible with local and SiS deployment."""
    return Path(__file__).parent


def get_logo_base64(logo_name="delta-dental-logo.webp"):
    """Load and encode logo as base64 for embedding in HTML."""
    app_root = get_app_root()
    logo_path = app_root / "assets" / logo_name
    if not logo_path.exists():
        logo_path = app_root / logo_name
    
    if logo_path.exists():
        with open(logo_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None


def get_snowflake_logo_base64():
    """Load and encode Snowflake logo as base64 for embedding in HTML."""
    app_root = get_app_root()
    # Try the new PNG logo first
    logo_path = app_root / "Snowflake-Logo.png"
    if logo_path.exists():
        with open(logo_path, "rb") as f:
            return base64.b64encode(f.read()).decode(), "png"
    
    # Fallback to assets folder
    logo_path = app_root / "assets" / "snowflake-logo.svg"
    if logo_path.exists():
        with open(logo_path, "r") as f:
            svg_content = f.read()
            return base64.b64encode(svg_content.encode()).decode(), "svg+xml"
    
    return None, None


def get_snowflake_icon_base64():
    """Load and encode Snowflake icon as base64 for embedding in HTML."""
    app_root = get_app_root()
    icon_path = app_root / "SNOW-ICON.png"
    if icon_path.exists():
        with open(icon_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None


def get_snowflake_logo_svg():
    """Return Snowflake logo SVG for embedding (legacy fallback)."""
    app_root = get_app_root()
    svg_path = app_root / "assets" / "snowflake-logo.svg"
    if svg_path.exists():
        with open(svg_path, "r") as f:
            return f.read()
    # Fallback inline SVG
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="40" height="40">
        <circle cx="50" cy="50" r="20" fill="#29B5E8"/>
        <rect x="48" y="10" width="4" height="30" fill="#29B5E8"/>
        <rect x="48" y="60" width="4" height="30" fill="#29B5E8"/>
        <rect x="48" y="10" width="4" height="30" fill="#29B5E8" transform="rotate(60 50 50)"/>
        <rect x="48" y="60" width="4" height="30" fill="#29B5E8" transform="rotate(60 50 50)"/>
        <rect x="48" y="10" width="4" height="30" fill="#29B5E8" transform="rotate(120 50 50)"/>
        <rect x="48" y="60" width="4" height="30" fill="#29B5E8" transform="rotate(120 50 50)"/>
    </svg>'''

# Import local modules
from data.sample_data import (
    MEMBER_COMPANIES, PRIORITIES, STATUSES, CATEGORIES, SUBCOMMITTEES,
    GOVERNANCE_TIERS, FINANCIAL_DATA, ONBOARDING_STATUS, PARTNERS,
    get_sample_use_cases, get_sample_contacts, get_sample_meetings,
    get_company_name, get_company_color,
    get_monthly_spend, get_investment_allocations, get_marketplace_drawdowns,
    get_scheduled_meetings
)
from utils.duplicate_detection import find_duplicates, calculate_similarity
from utils.export_utils import export_to_excel, generate_one_pager

# Page configuration
st.set_page_config(
    page_title="Delta Dental Project Tracker | DDPA × Snowflake",
    page_icon="🦷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful styling with Delta Dental branding
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    /* Brand Colors */
    :root {
        --delta-green: #39B54A;
        --delta-green-dark: #2D9340;
        --snowflake-blue: #29B5E8;
        --snowflake-blue-dark: #1A9FD1;
    }
    
    /* Global Styles */
    .stApp {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Header Styling - Delta Dental Green to Snowflake Blue gradient */
    .main-header {
        background: linear-gradient(135deg, #39B54A 0%, #2D9340 40%, #29B5E8 100%);
        padding: 1.5rem 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(57, 181, 74, 0.25);
    }
    
    .main-header-content {
        display: flex;
        align-items: center;
        gap: 1.5rem;
    }
    
    .main-header-logo {
        width: 70px;
        height: 70px;
        background: white;
        border-radius: 12px;
        padding: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    
    .main-header-logo img {
        width: 100%;
        height: 100%;
        object-fit: contain;
    }
    
    .main-header-text h1 {
        color: white;
        font-weight: 700;
        font-size: 1.75rem;
        margin: 0;
        letter-spacing: -0.02em;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .main-header-text p {
        color: rgba(255, 255, 255, 0.95);
        font-size: 0.95rem;
        margin: 0.25rem 0 0 0;
    }
    
    /* Co-branding badge */
    .co-brand {
        display: inline-flex;
        align-items: center;
        gap: 0.75rem;
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        padding: 0.5rem 1rem;
        border-radius: 50px;
        font-size: 0.85rem;
        color: white;
        margin-top: 0.75rem;
        font-weight: 500;
    }
    
    .co-brand-divider {
        width: 1px;
        height: 16px;
        background: rgba(255, 255, 255, 0.5);
    }
    
    /* Sidebar Logo */
    .sidebar-logo {
        text-align: center;
        padding: 1rem 0;
        margin-bottom: 1rem;
        border-bottom: 1px solid #e2e8f0;
    }
    
    .sidebar-logo img {
        width: 120px;
        border-radius: 8px;
    }
    
    /* Metric Cards - Updated with Delta Dental green */
    .metric-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 32px rgba(57, 181, 74, 0.12);
        border-color: #39B54A;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #39B54A;
        line-height: 1;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #64748b;
        margin-top: 0.5rem;
        font-weight: 500;
    }
    
    /* Status Pills */
    .status-pill {
        display: inline-block;
        padding: 0.35rem 0.9rem;
        border-radius: 50px;
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 0.02em;
    }
    
    .status-in-progress { background: #dbeafe; color: #1d4ed8; }
    .status-completed { background: #dcfce7; color: #166534; }
    .status-discovery { background: #fef3c7; color: #92400e; }
    .status-not-started { background: #f1f5f9; color: #475569; }
    .status-on-hold { background: #fee2e2; color: #dc2626; }
    
    /* Priority Badges */
    .priority-p0 { background: #fef2f2; color: #dc2626; border: 1px solid #fca5a5; }
    .priority-p1 { background: #fff7ed; color: #ea580c; border: 1px solid #fed7aa; }
    .priority-p2 { background: #fefce8; color: #ca8a04; border: 1px solid #fef08a; }
    .priority-p3 { background: #f0fdf4; color: #16a34a; border: 1px solid #bbf7d0; }
    
    /* Company Tags */
    .company-tag {
        display: inline-block;
        padding: 0.25rem 0.6rem;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
        margin: 0.15rem;
        background: #f1f5f9;
        color: #334155;
    }
    
    /* Cards - Updated hover with Delta Dental green */
    .use-case-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        transition: all 0.2s ease;
    }
    
    .use-case-card:hover {
        border-color: #39B54A;
        box-shadow: 0 8px 24px rgba(57, 181, 74, 0.15);
    }
    
    /* Duplicate Warning */
    .duplicate-warning {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border: 1px solid #f59e0b;
        border-radius: 12px;
        padding: 1rem 1.25rem;
        margin: 1rem 0;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .duplicate-warning-icon {
        font-size: 1.5rem;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
    }
    
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stMultiSelect label {
        font-weight: 600;
        color: #334155;
    }
    
    /* Section Headers */
    .section-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.75rem;
        border-bottom: 2px solid #39B54A;
    }
    
    .section-header h2 {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1e293b;
        margin: 0;
    }
    
    /* Progress Bar - Delta Dental green */
    .progress-container {
        background: #e2e8f0;
        border-radius: 50px;
        height: 8px;
        overflow: hidden;
    }
    
    .progress-bar {
        height: 100%;
        border-radius: 50px;
        transition: width 0.5s ease;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: #f8fafc;
        padding: 0.5rem;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* One Pager Styles - Updated with Delta Dental branding */
    .one-pager {
        background: white;
        border: 2px solid #e2e8f0;
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.06);
    }
    
    .one-pager-header {
        border-bottom: 3px solid #39B54A;
        padding-bottom: 1rem;
        margin-bottom: 1.5rem;
    }
    
    /* Partner logos section */
    .partner-logos {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 2rem;
        padding: 1rem;
        background: #f8fafc;
        border-radius: 12px;
        margin: 1rem 0;
    }
    
    .partner-logos img {
        height: 40px;
        object-fit: contain;
    }
</style>
""", unsafe_allow_html=True)


# Initialize session state
if 'use_cases' not in st.session_state:
    st.session_state.use_cases = get_sample_use_cases()
if 'contacts' not in st.session_state:
    st.session_state.contacts = get_sample_contacts()
if 'meetings' not in st.session_state:
    st.session_state.meetings = get_sample_meetings()
if 'selected_view' not in st.session_state:
    st.session_state.selected_view = "Dashboard"


def render_header():
    """Render the main header with co-branding and Delta Dental + Snowflake logos."""
    dd_logo_base64 = get_logo_base64()
    snow_logo_base64, snow_logo_type = get_snowflake_logo_base64()
    snow_icon_base64 = get_snowflake_icon_base64()
    
    if dd_logo_base64:
        dd_logo_html = f'<img src="data:image/webp;base64,{dd_logo_base64}" alt="Delta Dental">'
    else:
        dd_logo_html = '<span style="font-size: 2.5rem;">🦷</span>'
    
    if snow_icon_base64:
        snow_icon_html = f'<img src="data:image/png;base64,{snow_icon_base64}" alt="Snowflake" style="height: 28px; margin-left: 8px;">'
    else:
        snow_icon_html = '❄️'
    
    st.markdown(f"""
    <div class="main-header">
        <div class="main-header-content">
            <div class="main-header-logo">
                {dd_logo_html}
            </div>
            <div class="main-header-text">
                <h1>Delta Dental Project Planning Tracker</h1>
                <p>Collaborative Use Case & Roadmap Management Across Member Companies</p>
                <div class="co-brand">
                    <span style="font-weight: 600;">DDPA</span>
                    <div class="co-brand-divider"></div>
                    <span style="display: flex; align-items: center;">{snow_icon_html} <span style="margin-left: 6px;">Snowflake Partnership</span></span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_sidebar():
    """Render the sidebar navigation and filters."""
    with st.sidebar:
        # Display Delta Dental logo in sidebar
        app_root = get_app_root()
        dd_logo_path = app_root / "assets" / "delta-dental-logo.webp"
        if not dd_logo_path.exists():
            dd_logo_path = app_root / "delta-dental-logo.webp"
        
        if dd_logo_path.exists():
            st.image(str(dd_logo_path), use_container_width=True)
        
        st.markdown("### 🧭 Navigation")
        
        # Main navigation
        view_options = [
            "📊 Dashboard",
            "🏛️ Governance",
            "💰 Financial Tracking",
            "📋 Use Cases",
            "🗺️ Roadmap",
            "🏢 Member Companies",
            "👥 Contacts",
            "📅 Meetings",
            "🔍 Duplicate Detection",
            "📄 One-Pagers",
            "⚙️ Settings"
        ]
        
        selected = st.radio(
            "Select View",
            view_options,
            label_visibility="collapsed"
        )
        
        st.session_state.selected_view = selected.split(" ", 1)[1]
        
        st.markdown("---")
        
        # Filters
        st.markdown("### 🎯 Filters")
        
        # Company filter
        company_options = ["All Companies"] + [c["name"] for c in MEMBER_COMPANIES]
        selected_company = st.selectbox("Member Company", company_options)
        
        # Status filter
        status_options = ["All Statuses"] + STATUSES
        selected_status = st.selectbox("Status", status_options)
        
        # Priority filter
        priority_options = ["All Priorities"] + PRIORITIES
        selected_priority = st.selectbox("Priority", priority_options)
        
        # Category filter
        category_options = ["All Categories"] + CATEGORIES
        selected_category = st.selectbox("Category", category_options)
        
        st.markdown("---")
        
        # Quick stats
        st.markdown("### 📈 Quick Stats")
        df = st.session_state.use_cases
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Active", len(df[df['status'] == 'In Progress']))
        with col2:
            st.metric("Total", len(df))
        
        col3, col4 = st.columns(2)
        with col3:
            st.metric("P0/P1", len(df[df['priority'].isin(['P0 - Critical', 'P1 - High'])]))
        with col4:
            completed = len(df[df['status'] == 'Completed'])
            st.metric("Done", completed)
        
        # Partnership badge at bottom of sidebar
        st.markdown("---")
        snow_icon = get_snowflake_icon_base64()
        snow_icon_html = f'<img src="data:image/png;base64,{snow_icon}" style="height: 16px; vertical-align: middle;">' if snow_icon else '❄️'
        st.markdown(f"""
        <div style="text-align: center; padding: 0.5rem; background: linear-gradient(135deg, #39B54A15, #29B5E815); border-radius: 8px;">
            <div style="font-size: 0.7rem; color: #64748b; margin-bottom: 0.25rem;">Powered by</div>
            <div style="display: flex; justify-content: center; align-items: center; gap: 0.5rem;">
                <span style="color: #39B54A; font-weight: 600; font-size: 0.8rem;">DDPA</span>
                <span style="color: #cbd5e1;">×</span>
                <span style="color: #29B5E8; font-weight: 600; font-size: 0.8rem; display: flex; align-items: center; gap: 4px;">{snow_icon_html} Snowflake</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        return {
            'company': None if selected_company == "All Companies" else selected_company,
            'status': None if selected_status == "All Statuses" else selected_status,
            'priority': None if selected_priority == "All Priorities" else selected_priority,
            'category': None if selected_category == "All Categories" else selected_category
        }


def filter_use_cases(df, filters):
    """Apply filters to use cases dataframe."""
    filtered_df = df.copy()
    
    if filters['company']:
        company_id = None
        for c in MEMBER_COMPANIES:
            if c['name'] == filters['company']:
                company_id = c['id']
                break
        if company_id:
            filtered_df = filtered_df[
                (filtered_df['lead_company'] == company_id) |
                (filtered_df['participating_companies'].apply(lambda x: company_id in x))
            ]
    
    if filters['status']:
        filtered_df = filtered_df[filtered_df['status'] == filters['status']]
    
    if filters['priority']:
        filtered_df = filtered_df[filtered_df['priority'] == filters['priority']]
    
    if filters['category']:
        filtered_df = filtered_df[filtered_df['category'] == filters['category']]
    
    return filtered_df


def render_dashboard(filters):
    """Render the main dashboard view."""
    df = filter_use_cases(st.session_state.use_cases, filters)
    
    # Key Metrics
    st.markdown("### 📊 Key Metrics")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{len(df)}</div>
            <div class="metric-label">Total Use Cases</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        in_progress = len(df[df['status'] == 'In Progress'])
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: #1d4ed8;">{in_progress}</div>
            <div class="metric-label">In Progress</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        critical = len(df[df['priority'] == 'P0 - Critical'])
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: #dc2626;">{critical}</div>
            <div class="metric-label">Critical (P0)</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        avg_progress = df['progress'].mean() if len(df) > 0 else 0
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: #16a34a;">{avg_progress:.0f}%</div>
            <div class="metric-label">Avg Progress</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        companies_involved = len(set(df['lead_company'].tolist()))
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: #7c3aed;">{companies_involved}</div>
            <div class="metric-label">Companies Active</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Charts row
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Status Distribution")
        status_counts = df['status'].value_counts().reset_index()
        status_counts.columns = ['Status', 'Count']
        
        fig = px.pie(
            status_counts, 
            values='Count', 
            names='Status',
            color='Status',
            color_discrete_map={
                'In Progress': '#3b82f6',
                'Completed': '#22c55e',
                'Discovery': '#f59e0b',
                'Not Started': '#94a3b8',
                'On Hold': '#ef4444',
                'Cancelled': '#6b7280'
            },
            hole=0.4
        )
        fig.update_layout(
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.3),
            margin=dict(t=20, b=80, l=20, r=20),
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### Use Cases by Category")
        category_counts = df['category'].value_counts().reset_index()
        category_counts.columns = ['Category', 'Count']
        
        fig = px.bar(
            category_counts,
            x='Count',
            y='Category',
            orientation='h',
            color='Count',
            color_continuous_scale='Blues'
        )
        fig.update_layout(
            showlegend=False,
            margin=dict(t=20, b=20, l=20, r=20),
            height=300,
            yaxis={'categoryorder': 'total ascending'}
        )
        fig.update_coloraxes(showscale=False)
        st.plotly_chart(fig, use_container_width=True)
    
    # Company Activity
    st.markdown("#### 🏢 Activity by Member Company")
    
    company_stats = []
    for company in MEMBER_COMPANIES:
        company_df = df[
            (df['lead_company'] == company['id']) |
            (df['participating_companies'].apply(lambda x: company['id'] in x))
        ]
        leading = len(df[df['lead_company'] == company['id']])
        participating = len(company_df) - leading
        avg_prog = company_df['progress'].mean() if len(company_df) > 0 else 0
        
        company_stats.append({
            'Company': company['abbrev'],
            'Full Name': company['name'],
            'Leading': leading,
            'Participating': participating,
            'Total': len(company_df),
            'Avg Progress': f"{avg_prog:.0f}%",
            'Color': company['color']
        })
    
    company_df = pd.DataFrame(company_stats)
    
    fig = px.bar(
        company_df,
        x='Company',
        y=['Leading', 'Participating'],
        barmode='stack',
        color_discrete_sequence=['#0066B1', '#29B5E8'],
        labels={'value': 'Use Cases', 'variable': 'Role'}
    )
    fig.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(t=40, b=20, l=20, r=20),
        height=300
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Recent Activity / Priority Items
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🔥 Critical & High Priority")
        priority_df = df[df['priority'].isin(['P0 - Critical', 'P1 - High'])].head(5)
        
        for _, row in priority_df.iterrows():
            priority_class = "priority-p0" if "P0" in row['priority'] else "priority-p1"
            st.markdown(f"""
            <div class="use-case-card">
                <div style="display: flex; justify-content: space-between; align-items: start;">
                    <div>
                        <strong>{row['title']}</strong>
                        <div style="font-size: 0.85rem; color: #64748b; margin-top: 0.25rem;">
                            Lead: {get_company_name(row['lead_company'])}
                        </div>
                    </div>
                    <span class="status-pill {priority_class}">{row['priority'].split(' - ')[0]}</span>
                </div>
                <div class="progress-container" style="margin-top: 0.75rem;">
                    <div class="progress-bar" style="width: {row['progress']}%; background: linear-gradient(90deg, #0066B1, #29B5E8);"></div>
                </div>
                <div style="font-size: 0.75rem; color: #94a3b8; margin-top: 0.25rem;">{row['progress']}% complete</div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### ⚠️ Potential Duplicates")
        duplicates = find_duplicates(df)
        
        if duplicates:
            for dup in duplicates[:3]:
                st.markdown(f"""
                <div class="duplicate-warning">
                    <span class="duplicate-warning-icon">⚠️</span>
                    <div>
                        <strong>Similar Use Cases Detected</strong>
                        <div style="font-size: 0.85rem; margin-top: 0.25rem;">
                            "{dup['title1']}" and "{dup['title2']}"
                            <br><span style="color: #92400e;">Similarity: {dup['similarity']:.0%}</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No potential duplicates detected.")


def render_use_case_form(use_case=None, form_key="use_case_form"):
    """Render a form for adding/editing a use case. Returns the form data if submitted."""
    is_edit = use_case is not None
    
    with st.form(form_key):
        col1, col2 = st.columns(2)
        with col1:
            title = st.text_input("Title*", value=use_case['title'] if is_edit else "")
            category = st.selectbox(
                "Category*", 
                CATEGORIES,
                index=CATEGORIES.index(use_case['category']) if is_edit and use_case['category'] in CATEGORIES else 0
            )
            priority = st.selectbox(
                "Priority*", 
                PRIORITIES,
                index=PRIORITIES.index(use_case['priority']) if is_edit and use_case['priority'] in PRIORITIES else 0
            )
            lead_company = st.selectbox(
                "Lead Company*",
                [c['id'] for c in MEMBER_COMPANIES],
                index=[c['id'] for c in MEMBER_COMPANIES].index(use_case['lead_company']) if is_edit else 0,
                format_func=lambda x: get_company_name(x)
            )
        with col2:
            description = st.text_area("Description", value=use_case['description'] if is_edit else "")
            status = st.selectbox(
                "Status", 
                STATUSES,
                index=STATUSES.index(use_case['status']) if is_edit and use_case['status'] in STATUSES else 0
            )
            participating = st.multiselect(
                "Participating Companies",
                [c['id'] for c in MEMBER_COMPANIES],
                default=use_case['participating_companies'] if is_edit else [],
                format_func=lambda x: get_company_name(x)
            )
            subcommittee = st.selectbox(
                "Subcommittee", 
                SUBCOMMITTEES,
                index=SUBCOMMITTEES.index(use_case['subcommittee']) if is_edit and use_case['subcommittee'] in SUBCOMMITTEES else 0
            )
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            start_date = st.date_input(
                "Start Date",
                value=datetime.strptime(use_case['start_date'], "%Y-%m-%d") if is_edit else datetime.now()
            )
        with col2:
            target_date = st.date_input(
                "Target Date",
                value=datetime.strptime(use_case['target_date'], "%Y-%m-%d") if is_edit else datetime.now() + timedelta(days=90)
            )
        with col3:
            progress = st.slider("Progress %", 0, 100, value=use_case['progress'] if is_edit else 0)
        with col4:
            estimated_value = st.text_input(
                "Estimated Value", 
                value=use_case['estimated_value'] if is_edit else "",
                placeholder="e.g., $1.5M"
            )
        
        tags_str = st.text_input(
            "Tags (comma-separated)",
            value=", ".join(use_case['tags']) if is_edit and use_case.get('tags') else ""
        )
        
        col1, col2 = st.columns(2)
        with col1:
            submitted = st.form_submit_button(
                "💾 Save Changes" if is_edit else "➕ Create Use Case", 
                use_container_width=True,
                type="primary"
            )
        with col2:
            cancelled = st.form_submit_button("❌ Cancel", use_container_width=True)
        
        if cancelled:
            return "cancel"
        
        if submitted and title:
            return {
                "title": title,
                "description": description,
                "category": category,
                "priority": priority,
                "status": status,
                "lead_company": lead_company,
                "participating_companies": participating,
                "start_date": start_date.strftime("%Y-%m-%d"),
                "target_date": target_date.strftime("%Y-%m-%d"),
                "progress": progress,
                "estimated_value": estimated_value,
                "tags": [t.strip() for t in tags_str.split(",") if t.strip()],
                "subcommittee": subcommittee
            }
    
    return None


def render_use_cases(filters):
    """Render the use cases list view with full CRUD capabilities."""
    df = filter_use_cases(st.session_state.use_cases, filters)
    
    st.markdown("### 📋 Use Cases Management")
    
    # View mode tabs
    tab1, tab2, tab3 = st.tabs(["📋 View All", "➕ Add New", "✏️ Edit/Delete"])
    
    with tab1:
        # Action buttons
        col1, col2, col3 = st.columns([1, 1, 4])
        with col1:
            view_type = st.selectbox("View", ["Cards", "Table", "Editable Grid"], label_visibility="collapsed")
        with col2:
            st.download_button(
                "📥 Export Excel",
                export_to_excel(df),
                file_name="use_cases_export.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        
        if view_type == "Cards":
            for idx, row in df.iterrows():
                status_class = f"status-{row['status'].lower().replace(' ', '-')}"
                priority_class = f"priority-{row['priority'].split(' ')[0].lower()}"
                
                with st.container():
                    col1, col2, col3 = st.columns([4, 1, 0.5])
                    
                    with col1:
                        st.markdown(f"**{row['id']}** | {row['title']}")
                        st.caption(f"{row['description'][:150]}..." if len(str(row['description'])) > 150 else row['description'])
                        
                        companies_html = " ".join([
                            f'<span class="company-tag" style="background: {get_company_color(c)}20; color: {get_company_color(c)};">{c}</span>'
                            for c in row['participating_companies']
                        ])
                        st.markdown(f"""
                        <div style="margin: 0.5rem 0;">
                            <span class="status-pill {status_class}">{row['status']}</span>
                            <span class="status-pill {priority_class}" style="margin-left: 0.5rem;">{row['priority']}</span>
                        </div>
                        <div style="margin-top: 0.5rem;">
                            <strong style="font-size: 0.8rem; color: #64748b;">Lead:</strong> {companies_html}
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown(f"""
                        <div style="text-align: center;">
                            <div style="font-size: 2rem; font-weight: 700; color: #39B54A;">{row['progress']}%</div>
                            <div style="font-size: 0.75rem; color: #94a3b8;">Progress</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col3:
                        if st.button("✏️", key=f"edit_card_{row['id']}", help="Edit this use case"):
                            st.session_state.editing_use_case = row['id']
                            st.rerun()
                    
                    st.markdown("---")
        
        elif view_type == "Table":
            display_df = df[['id', 'title', 'category', 'priority', 'status', 'lead_company', 'progress', 'target_date']].copy()
            display_df['lead_company'] = display_df['lead_company'].apply(get_company_name)
            display_df.columns = ['ID', 'Title', 'Category', 'Priority', 'Status', 'Lead Company', 'Progress', 'Target Date']
            
            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Progress": st.column_config.ProgressColumn("Progress", min_value=0, max_value=100, format="%d%%")
                }
            )
        
        else:  # Editable Grid
            st.info("💡 Edit cells directly in the table below. Changes are saved automatically when you modify a cell.")
            
            # Prepare editable dataframe
            edit_df = df[['id', 'title', 'category', 'priority', 'status', 'lead_company', 'progress', 'estimated_value']].copy()
            
            edited_df = st.data_editor(
                edit_df,
                use_container_width=True,
                hide_index=True,
                num_rows="fixed",
                column_config={
                    "id": st.column_config.TextColumn("ID", disabled=True),
                    "title": st.column_config.TextColumn("Title", width="large"),
                    "category": st.column_config.SelectboxColumn("Category", options=CATEGORIES, required=True),
                    "priority": st.column_config.SelectboxColumn("Priority", options=PRIORITIES, required=True),
                    "status": st.column_config.SelectboxColumn("Status", options=STATUSES, required=True),
                    "lead_company": st.column_config.SelectboxColumn(
                        "Lead Company", 
                        options=[c['id'] for c in MEMBER_COMPANIES],
                        required=True
                    ),
                    "progress": st.column_config.NumberColumn("Progress %", min_value=0, max_value=100, step=5),
                    "estimated_value": st.column_config.TextColumn("Est. Value")
                },
                key="use_cases_editor"
            )
            
            # Check if data changed
            if not edited_df.equals(edit_df):
                # Update the main dataframe
                for idx, row in edited_df.iterrows():
                    uc_idx = st.session_state.use_cases[st.session_state.use_cases['id'] == row['id']].index
                    if len(uc_idx) > 0:
                        for col in ['title', 'category', 'priority', 'status', 'lead_company', 'progress', 'estimated_value']:
                            st.session_state.use_cases.loc[uc_idx[0], col] = row[col]
                st.success("✅ Changes saved!")
    
    with tab2:
        st.markdown("#### ➕ Add New Use Case")
        
        result = render_use_case_form(form_key="add_use_case_form")
        
        if result == "cancel":
            st.rerun()
        elif result:
            new_id = f"UC{len(st.session_state.use_cases) + 1:03d}"
            result['id'] = new_id
            st.session_state.use_cases = pd.concat([
                st.session_state.use_cases,
                pd.DataFrame([result])
            ], ignore_index=True)
            st.success(f"✅ Use case '{result['title']}' created successfully!")
            st.rerun()
    
    with tab3:
        st.markdown("#### ✏️ Edit or Delete Use Cases")
        
        # Select use case to edit
        use_case_options = {row['id']: f"{row['id']}: {row['title']}" for _, row in st.session_state.use_cases.iterrows()}
        
        selected_id = st.selectbox(
            "Select Use Case to Edit",
            options=list(use_case_options.keys()),
            format_func=lambda x: use_case_options[x],
            key="select_edit_uc"
        )
        
        if selected_id:
            use_case = st.session_state.use_cases[st.session_state.use_cases['id'] == selected_id].iloc[0].to_dict()
            
            # Delete button
            col1, col2 = st.columns([4, 1])
            with col2:
                if st.button("🗑️ Delete", type="secondary", use_container_width=True):
                    st.session_state.confirm_delete = selected_id
            
            # Confirm delete dialog
            if st.session_state.get('confirm_delete') == selected_id:
                st.warning(f"⚠️ Are you sure you want to delete '{use_case['title']}'?")
                col1, col2, col3 = st.columns([1, 1, 2])
                with col1:
                    if st.button("Yes, Delete", type="primary"):
                        st.session_state.use_cases = st.session_state.use_cases[
                            st.session_state.use_cases['id'] != selected_id
                        ].reset_index(drop=True)
                        st.session_state.confirm_delete = None
                        st.success("✅ Use case deleted!")
                        st.rerun()
                with col2:
                    if st.button("Cancel"):
                        st.session_state.confirm_delete = None
                        st.rerun()
            else:
                # Edit form
                result = render_use_case_form(use_case=use_case, form_key=f"edit_uc_{selected_id}")
                
                if result == "cancel":
                    st.rerun()
                elif result:
                    # Update the use case
                    idx = st.session_state.use_cases[st.session_state.use_cases['id'] == selected_id].index[0]
                    for key, value in result.items():
                        st.session_state.use_cases.loc[idx, key] = value
                    st.success(f"✅ Use case '{result['title']}' updated successfully!")
                    st.rerun()


def render_roadmap(filters):
    """Render the roadmap/Gantt chart view."""
    df = filter_use_cases(st.session_state.use_cases, filters)
    
    st.markdown("### 🗺️ Master Roadmap")
    st.caption("Timeline view of all use cases across member companies")
    
    # Prepare data for Gantt chart
    gantt_data = []
    for _, row in df.iterrows():
        gantt_data.append({
            'Task': f"{row['id']}: {row['title'][:40]}...",
            'Start': row['start_date'],
            'Finish': row['target_date'],
            'Company': get_company_name(row['lead_company']),
            'Status': row['status'],
            'Priority': row['priority'],
            'Progress': row['progress'],
            'Color': get_company_color(row['lead_company'])
        })
    
    gantt_df = pd.DataFrame(gantt_data)
    
    if len(gantt_df) > 0:
        # View options
        col1, col2 = st.columns([1, 4])
        with col1:
            color_by = st.selectbox("Color by", ["Company", "Status", "Priority"])
        
        color_map = {
            'Company': {get_company_name(c['id']): c['color'] for c in MEMBER_COMPANIES},
            'Status': {
                'In Progress': '#3b82f6',
                'Completed': '#22c55e',
                'Discovery': '#f59e0b',
                'Not Started': '#94a3b8',
                'On Hold': '#ef4444',
                'Cancelled': '#6b7280'
            },
            'Priority': {
                'P0 - Critical': '#dc2626',
                'P1 - High': '#ea580c',
                'P2 - Medium': '#ca8a04',
                'P3 - Low': '#16a34a'
            }
        }
        
        fig = px.timeline(
            gantt_df,
            x_start='Start',
            x_end='Finish',
            y='Task',
            color=color_by,
            color_discrete_map=color_map[color_by],
            hover_data=['Status', 'Priority', 'Progress']
        )
        
        fig.update_layout(
            height=max(400, len(gantt_df) * 40),
            xaxis_title="Timeline",
            yaxis_title="",
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=20, r=20, t=60, b=20)
        )
        
        fig.update_yaxes(categoryorder='array', categoryarray=gantt_df['Task'].tolist()[::-1])
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Quarterly summary
        st.markdown("#### 📅 Quarterly Breakdown")
        
        col1, col2, col3, col4 = st.columns(4)
        quarters = ['Q1 2024', 'Q2 2024', 'Q3 2024', 'Q4 2024']
        
        for i, (col, q) in enumerate(zip([col1, col2, col3, col4], quarters)):
            with col:
                # Count use cases with target dates in this quarter
                q_start = datetime(2024, i*3 + 1, 1)
                q_end = datetime(2024, (i+1)*3 if i < 3 else 12, 28)
                
                q_count = len(df[
                    (pd.to_datetime(df['target_date']) >= q_start) &
                    (pd.to_datetime(df['target_date']) <= q_end)
                ])
                
                st.metric(q, f"{q_count} deliverables")
    else:
        st.info("No use cases match the current filters.")


def render_member_companies():
    """Render individual member company views with editable capabilities."""
    st.markdown("### 🏢 Member Companies")
    
    # Initialize member companies in session state if not exists
    if 'member_companies' not in st.session_state:
        st.session_state.member_companies = pd.DataFrame(MEMBER_COMPANIES)
    
    # Get current member companies from session state
    member_companies_list = st.session_state.member_companies.to_dict('records')
    
    # Add tabs for each company plus Association, National Platform, and Edit
    tab_names = [c['abbrev'] for c in member_companies_list] + ["DDPA Association", "National Platform", "✏️ Edit Companies"]
    tabs = st.tabs(tab_names)
    
    df = st.session_state.use_cases
    contacts_df = st.session_state.contacts
    
    for i, tab in enumerate(tabs):
        with tab:
            # Edit tab (last tab)
            if i == len(tabs) - 1:
                st.markdown("#### ✏️ Manage Member Companies")
                st.info("💡 Add, edit, or remove member companies. Changes will affect all company-related dropdowns throughout the app.")
                
                # Add new company button
                if st.button("➕ Add New Member Company"):
                    new_company = {
                        "id": f"NEW{len(st.session_state.member_companies) + 1}",
                        "name": "New Delta Dental Company",
                        "abbrev": "DDNEW",
                        "region": "West",
                        "color": "#6B7280"
                    }
                    st.session_state.member_companies = pd.concat([
                        st.session_state.member_companies,
                        pd.DataFrame([new_company])
                    ], ignore_index=True)
                    st.rerun()
                
                # Editable grid
                edited_companies = st.data_editor(
                    st.session_state.member_companies,
                    use_container_width=True,
                    hide_index=True,
                    num_rows="dynamic",
                    column_config={
                        "id": st.column_config.TextColumn(
                            "ID", 
                            help="Unique identifier (used in data references)",
                            width="small"
                        ),
                        "name": st.column_config.TextColumn(
                            "Full Name",
                            help="Full company name",
                            width="large"
                        ),
                        "abbrev": st.column_config.TextColumn(
                            "Abbreviation",
                            help="Short display name",
                            width="small"
                        ),
                        "region": st.column_config.SelectboxColumn(
                            "Region",
                            options=["West", "Northeast", "South", "Midwest", "Southeast", "Northwest"],
                            required=True,
                            width="small"
                        ),
                        "color": st.column_config.TextColumn(
                            "Brand Color",
                            help="Hex color code (e.g., #1E88E5)",
                            width="small"
                        )
                    },
                    key="member_companies_editor"
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("💾 Save Member Companies", type="primary", use_container_width=True):
                        st.session_state.member_companies = edited_companies
                        st.success("✅ Member companies saved!")
                        st.rerun()
                with col2:
                    if st.button("🔄 Reset to Defaults", type="secondary", use_container_width=True):
                        st.session_state.member_companies = pd.DataFrame(MEMBER_COMPANIES)
                        st.success("✅ Reset to default member companies!")
                        st.rerun()
                
                # Color preview
                st.markdown("---")
                st.markdown("##### 🎨 Color Preview")
                cols = st.columns(len(edited_companies))
                for idx, (_, company) in enumerate(edited_companies.iterrows()):
                    with cols[idx % len(cols)]:
                        color = company.get('color', '#6B7280')
                        st.markdown(f"""
                        <div style="background: {color}; color: white; padding: 0.5rem; 
                                    border-radius: 8px; text-align: center; font-weight: 600;">
                            {company.get('abbrev', 'N/A')}
                        </div>
                        """, unsafe_allow_html=True)
                
                continue
            
            # Regular company tabs
            if i < len(member_companies_list):
                company = member_companies_list[i]
                company_id = company['id']
                company_name = company['name']
                color = company['color']
            elif i == len(member_companies_list):
                company_id = "ASSOC"
                company_name = "DDPA Association"
                color = "#2C3E50"
            else:
                company_id = "NATIONAL"
                company_name = "National Data Platform"
                color = "#0066B1"
            
            # Header
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, {color}15, {color}05); 
                        border-left: 4px solid {color}; padding: 1.5rem; border-radius: 12px; margin-bottom: 1.5rem;">
                <h2 style="margin: 0; color: {color};">{company_name}</h2>
            </div>
            """, unsafe_allow_html=True)
            
            if i < len(member_companies_list):
                # Stats for member company
                company_uc = df[
                    (df['lead_company'] == company_id) |
                    (df['participating_companies'].apply(lambda x: company_id in x))
                ]
                
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Leading", len(df[df['lead_company'] == company_id]))
                col2.metric("Participating", len(company_uc) - len(df[df['lead_company'] == company_id]))
                col3.metric("In Progress", len(company_uc[company_uc['status'] == 'In Progress']))
                col4.metric("Avg Progress", f"{company_uc['progress'].mean():.0f}%" if len(company_uc) > 0 else "0%")
                
                # Sub-tabs for contacts and use cases with edit capability
                sub_tabs = st.tabs(["👥 Contacts", "📋 Use Cases", "✏️ Quick Edit"])
                
                with sub_tabs[0]:
                    # Contacts
                    st.markdown("##### 👥 Key Contacts")
                    company_contacts = contacts_df[contacts_df['company'] == company_id]
                    if len(company_contacts) > 0:
                        for _, contact in company_contacts.iterrows():
                            primary_badge = "🌟 " if contact['is_primary'] else ""
                            st.markdown(f"""
                            **{primary_badge}{contact['name']}** - {contact['role']}  
                            📧 {contact['email']} | 📞 {contact['phone']}
                            """)
                    else:
                        st.caption("No contacts assigned to this company")
                        if st.button(f"➕ Add Contact for {company_name}", key=f"add_contact_{company_id}"):
                            st.info("Go to Contacts section to add a new contact")
                
                with sub_tabs[1]:
                    # Use cases
                    st.markdown("##### 📋 Use Cases")
                    if len(company_uc) > 0:
                        for _, uc in company_uc.iterrows():
                            role = "Lead" if uc['lead_company'] == company_id else "Participant"
                            role_color = "#16a34a" if role == "Lead" else "#3b82f6"
                            st.markdown(f"""
                            <div style="display: flex; justify-content: space-between; padding: 0.75rem; 
                                        background: #f8fafc; border-radius: 8px; margin-bottom: 0.5rem;">
                                <div>
                                    <strong>{uc['id']}</strong>: {uc['title']}
                                    <span style="background: {role_color}20; color: {role_color}; 
                                                padding: 0.2rem 0.5rem; border-radius: 4px; 
                                                font-size: 0.75rem; margin-left: 0.5rem;">{role}</span>
                                </div>
                                <span style="color: #64748b;">{uc['status']} | {uc['progress']}%</span>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.caption("No use cases assigned to this company")
                
                with sub_tabs[2]:
                    # Quick edit for company-specific data
                    st.markdown("##### ✏️ Quick Edit Company Data")
                    
                    # Edit company info
                    with st.form(f"edit_company_{company_id}"):
                        st.markdown("**Company Information**")
                        col1, col2 = st.columns(2)
                        with col1:
                            new_name = st.text_input("Full Name", value=company_name)
                            new_abbrev = st.text_input("Abbreviation", value=company.get('abbrev', ''))
                        with col2:
                            new_region = st.selectbox(
                                "Region",
                                options=["West", "Northeast", "South", "Midwest", "Southeast", "Northwest"],
                                index=["West", "Northeast", "South", "Midwest", "Southeast", "Northwest"].index(company.get('region', 'West')) if company.get('region', 'West') in ["West", "Northeast", "South", "Midwest", "Southeast", "Northwest"] else 0
                            )
                            new_color = st.color_picker("Brand Color", value=color)
                        
                        if st.form_submit_button("💾 Save Company Info", use_container_width=True):
                            # Update the company in session state
                            idx = st.session_state.member_companies[st.session_state.member_companies['id'] == company_id].index
                            if len(idx) > 0:
                                st.session_state.member_companies.loc[idx[0], 'name'] = new_name
                                st.session_state.member_companies.loc[idx[0], 'abbrev'] = new_abbrev
                                st.session_state.member_companies.loc[idx[0], 'region'] = new_region
                                st.session_state.member_companies.loc[idx[0], 'color'] = new_color
                                st.success(f"✅ {new_name} updated successfully!")
                                st.rerun()
                    
                    # Quick edit use case progress for this company
                    st.markdown("---")
                    st.markdown("**Quick Update Use Case Progress**")
                    if len(company_uc) > 0:
                        progress_updates = {}
                        for _, uc in company_uc.iterrows():
                            col1, col2 = st.columns([3, 1])
                            with col1:
                                st.caption(f"{uc['id']}: {uc['title']}")
                            with col2:
                                progress_updates[uc['id']] = st.slider(
                                    "Progress",
                                    0, 100, int(uc['progress']),
                                    key=f"progress_{company_id}_{uc['id']}",
                                    label_visibility="collapsed"
                                )
                        
                        if st.button("💾 Save Progress Updates", key=f"save_progress_{company_id}"):
                            for uc_id, progress in progress_updates.items():
                                idx = st.session_state.use_cases[st.session_state.use_cases['id'] == uc_id].index
                                if len(idx) > 0:
                                    st.session_state.use_cases.loc[idx[0], 'progress'] = progress
                            st.success("✅ Progress updated!")
                            st.rerun()
                    else:
                        st.caption("No use cases to update")
            
            elif company_id == "NATIONAL":
                # National Platform - show all cross-company initiatives
                st.markdown("##### 🌐 Cross-Company Initiatives")
                national_uc = df[df['participating_companies'].apply(lambda x: len(x) >= 3)]
                
                col1, col2 = st.columns(2)
                col1.metric("Multi-Company Projects", len(national_uc))
                col2.metric("Companies Involved", len(member_companies_list))
                
                for _, uc in national_uc.iterrows():
                    companies = ", ".join([get_company_name(c) for c in uc['participating_companies']])
                    st.markdown(f"""
                    **{uc['id']}: {uc['title']}**  
                    Companies: {companies}  
                    Status: {uc['status']} | Progress: {uc['progress']}%
                    """)
                    st.markdown("---")


def render_contacts():
    """Render the contacts management view with editable data."""
    st.markdown("### 👥 Contacts & Subcommittees")
    
    contacts_df = st.session_state.contacts
    
    tab1, tab2, tab3 = st.tabs(["📇 View Contacts", "✏️ Edit Contacts", "🏛️ Subcommittees"])
    
    with tab1:
        # Filters
        col1, col2 = st.columns([1, 4])
        with col1:
            company_filter = st.selectbox(
                "Filter by Company",
                ["All"] + [c['name'] for c in MEMBER_COMPANIES] + ["DDPA Association", "Snowflake"],
                key="contact_filter_view"
            )
        
        # Apply filter
        filtered_contacts = contacts_df.copy()
        if company_filter != "All":
            if company_filter == "DDPA Association":
                filtered_contacts = filtered_contacts[filtered_contacts['company'] == 'ASSOC']
            elif company_filter == "Snowflake":
                filtered_contacts = filtered_contacts[filtered_contacts['company'] == 'SNOWFLAKE']
            else:
                company_id = None
                for c in MEMBER_COMPANIES:
                    if c['name'] == company_filter:
                        company_id = c['id']
                        break
                if company_id:
                    filtered_contacts = filtered_contacts[filtered_contacts['company'] == company_id]
        
        # Display contacts as cards
        for _, contact in filtered_contacts.iterrows():
            company_name = get_company_name(contact['company'])
            primary_icon = "⭐" if contact['is_primary'] else ""
            
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                st.markdown(f"**{primary_icon} {contact['name']}**")
                st.caption(contact['role'])
            with col2:
                st.markdown(f"📧 {contact['email']}")
                st.caption(f"📞 {contact['phone']}")
            with col3:
                st.markdown(f"🏢 {company_name}")
                subcommittees = ", ".join(contact['subcommittees'][:2]) if contact['subcommittees'] else ""
                st.caption(subcommittees if subcommittees else "No committees")
            
            st.markdown("---")
    
    with tab2:
        st.info("💡 Edit contact information directly in the table. Changes are saved when you modify a cell.")
        
        # Add new contact button
        if st.button("➕ Add New Contact"):
            new_id = f"C{len(st.session_state.contacts) + 1:03d}"
            new_contact = {
                "id": new_id,
                "name": "New Contact",
                "role": "Role",
                "company": "CA",
                "email": "email@deltadental.com",
                "phone": "(555) 555-0000",
                "is_primary": False,
                "subcommittees": []
            }
            st.session_state.contacts = pd.concat([
                st.session_state.contacts,
                pd.DataFrame([new_contact])
            ], ignore_index=True)
            st.rerun()
        
        # Prepare editable dataframe
        company_options = [c['id'] for c in MEMBER_COMPANIES] + ['ASSOC', 'SNOWFLAKE']
        
        # Create a display copy with subcommittees as string
        edit_df = contacts_df.copy()
        edit_df['subcommittees_str'] = edit_df['subcommittees'].apply(
            lambda x: ", ".join(x) if isinstance(x, list) else ""
        )
        
        edited_contacts = st.data_editor(
            edit_df[['id', 'name', 'role', 'company', 'email', 'phone', 'is_primary', 'subcommittees_str']],
            use_container_width=True,
            hide_index=True,
            num_rows="dynamic",
            column_config={
                "id": st.column_config.TextColumn("ID", disabled=True, width="small"),
                "name": st.column_config.TextColumn("Name", width="medium"),
                "role": st.column_config.TextColumn("Role", width="medium"),
                "company": st.column_config.SelectboxColumn(
                    "Company",
                    options=company_options,
                    required=True,
                    width="small"
                ),
                "email": st.column_config.TextColumn("Email", width="medium"),
                "phone": st.column_config.TextColumn("Phone", width="small"),
                "is_primary": st.column_config.CheckboxColumn("Primary?", width="small"),
                "subcommittees_str": st.column_config.TextColumn(
                    "Subcommittees (comma-separated)", 
                    width="large",
                    help="Enter subcommittees separated by commas"
                )
            },
            key="contacts_editor"
        )
        
        # Save changes button
        if st.button("💾 Save All Changes", type="primary"):
            # Update the contacts dataframe
            for idx, row in edited_contacts.iterrows():
                if idx < len(st.session_state.contacts):
                    st.session_state.contacts.loc[idx, 'name'] = row['name']
                    st.session_state.contacts.loc[idx, 'role'] = row['role']
                    st.session_state.contacts.loc[idx, 'company'] = row['company']
                    st.session_state.contacts.loc[idx, 'email'] = row['email']
                    st.session_state.contacts.loc[idx, 'phone'] = row['phone']
                    st.session_state.contacts.loc[idx, 'is_primary'] = row['is_primary']
                    # Parse subcommittees string back to list
                    subcommittees = [s.strip() for s in row['subcommittees_str'].split(",") if s.strip()]
                    st.session_state.contacts.at[idx, 'subcommittees'] = subcommittees
            st.success("✅ Contacts saved successfully!")
            st.rerun()
        
        # Delete contact section
        st.markdown("---")
        st.markdown("##### 🗑️ Delete Contact")
        contact_to_delete = st.selectbox(
            "Select contact to delete",
            options=contacts_df['id'].tolist(),
            format_func=lambda x: f"{x}: {contacts_df[contacts_df['id']==x]['name'].iloc[0]}"
        )
        if st.button("Delete Selected Contact", type="secondary"):
            st.session_state.contacts = st.session_state.contacts[
                st.session_state.contacts['id'] != contact_to_delete
            ].reset_index(drop=True)
            st.success("✅ Contact deleted!")
            st.rerun()
    
    with tab3:
        for subcommittee in SUBCOMMITTEES:
            with st.expander(f"🏛️ {subcommittee}"):
                members = contacts_df[contacts_df['subcommittees'].apply(
                    lambda x: subcommittee in x if isinstance(x, list) else False
                )]
                if len(members) > 0:
                    for _, member in members.iterrows():
                        company_name = get_company_name(member['company'])
                        st.markdown(f"• **{member['name']}** ({company_name}) - {member['role']}")
                else:
                    st.caption("No members assigned")


def render_duplicate_detection():
    """Render the duplicate detection view."""
    st.markdown("### 🔍 Duplicate & Overlap Detection")
    st.caption("Identify similar use cases and potential consolidation opportunities")
    
    df = st.session_state.use_cases
    duplicates = find_duplicates(df, threshold=0.3)
    
    if duplicates:
        st.warning(f"⚠️ Found {len(duplicates)} potential duplicate/overlapping use cases")
        
        for dup in duplicates:
            similarity_color = "#dc2626" if dup['similarity'] > 0.7 else "#f59e0b" if dup['similarity'] > 0.5 else "#3b82f6"
            
            st.markdown(f"""
            <div style="background: white; border: 2px solid {similarity_color}40; border-radius: 12px; 
                        padding: 1.5rem; margin-bottom: 1rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <h4 style="margin: 0; color: {similarity_color};">
                        ⚠️ {dup['similarity']:.0%} Similar
                    </h4>
                    <span style="background: {similarity_color}20; color: {similarity_color}; 
                                padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.85rem;">
                        {'High' if dup['similarity'] > 0.7 else 'Medium' if dup['similarity'] > 0.5 else 'Low'} Risk
                    </span>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                    <div style="background: #f8fafc; padding: 1rem; border-radius: 8px;">
                        <strong>{dup['id1']}</strong>: {dup['title1']}<br>
                        <span style="color: #64748b; font-size: 0.85rem;">
                            Lead: {get_company_name(dup['company1'])} | Status: {dup['status1']}
                        </span>
                    </div>
                    <div style="background: #f8fafc; padding: 1rem; border-radius: 8px;">
                        <strong>{dup['id2']}</strong>: {dup['title2']}<br>
                        <span style="color: #64748b; font-size: 0.85rem;">
                            Lead: {get_company_name(dup['company2'])} | Status: {dup['status2']}
                        </span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button(f"🔗 Merge into {dup['id1']}", key=f"merge_{dup['id1']}_{dup['id2']}"):
                    st.info("Merge functionality would combine these use cases")
            with col2:
                if st.button(f"✅ Mark as Distinct", key=f"distinct_{dup['id1']}_{dup['id2']}"):
                    st.success("Marked as intentionally distinct")
            with col3:
                if st.button(f"📋 Create Review Task", key=f"review_{dup['id1']}_{dup['id2']}"):
                    st.success("Review task created for next steering committee")
    else:
        st.success("✅ No significant duplicates detected! All use cases appear distinct.")
    
    # Category overlap analysis
    st.markdown("---")
    st.markdown("#### 📊 Category Overlap by Company")
    
    # Build overlap matrix
    overlap_data = []
    for cat in CATEGORIES:
        cat_data = {'Category': cat}
        for company in MEMBER_COMPANIES:
            count = len(df[
                (df['category'] == cat) &
                ((df['lead_company'] == company['id']) |
                 (df['participating_companies'].apply(lambda x: company['id'] in x)))
            ])
            cat_data[company['abbrev']] = count
        overlap_data.append(cat_data)
    
    overlap_df = pd.DataFrame(overlap_data)
    overlap_df = overlap_df.set_index('Category')
    
    fig = px.imshow(
        overlap_df.values,
        x=overlap_df.columns,
        y=overlap_df.index,
        color_continuous_scale='Blues',
        labels=dict(x="Company", y="Category", color="Use Cases")
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)


def render_one_pagers():
    """Render one-pager generation view."""
    st.markdown("### 📄 One-Pager Summaries")
    st.caption("Generate executive summaries for member companies and initiatives")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("#### Generate One-Pager")
        
        pager_type = st.selectbox(
            "One-Pager Type",
            ["Member Company", "Use Case", "Subcommittee", "National Platform"]
        )
        
        if pager_type == "Member Company":
            selection = st.selectbox(
                "Select Company",
                [c['name'] for c in MEMBER_COMPANIES]
            )
        elif pager_type == "Use Case":
            selection = st.selectbox(
                "Select Use Case",
                st.session_state.use_cases['title'].tolist()
            )
        elif pager_type == "Subcommittee":
            selection = st.selectbox("Select Subcommittee", SUBCOMMITTEES)
        else:
            selection = "National Data Platform"
        
        if st.button("📄 Generate One-Pager", use_container_width=True):
            st.session_state.generated_pager = {
                'type': pager_type,
                'selection': selection
            }
    
    with col2:
        if st.session_state.get('generated_pager'):
            pager = st.session_state.generated_pager
            
            # Find company details
            if pager['type'] == "Member Company":
                company = next((c for c in MEMBER_COMPANIES if c['name'] == pager['selection']), None)
                company_id = company['id'] if company else None
                color = company['color'] if company else "#0066B1"
                
                df = st.session_state.use_cases
                company_uc = df[
                    (df['lead_company'] == company_id) |
                    (df['participating_companies'].apply(lambda x: company_id in x if company_id else False))
                ]
                contacts = st.session_state.contacts[st.session_state.contacts['company'] == company_id]
                primary_contact = contacts[contacts['is_primary'] == True].iloc[0] if len(contacts[contacts['is_primary'] == True]) > 0 else None
                
                st.markdown(f"""
                <div class="one-pager">
                    <div class="one-pager-header">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <h2 style="margin: 0; color: {color};">{pager['selection']}</h2>
                                <p style="color: #64748b; margin: 0.5rem 0 0 0;">Member Company Overview</p>
                            </div>
                            <div style="text-align: right; font-size: 0.85rem; color: #64748b;">
                                DDPA × Snowflake<br>
                                {datetime.now().strftime('%B %Y')}
                            </div>
                        </div>
                    </div>
                    
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem;">
                        <div>
                            <h4 style="color: {color}; margin-bottom: 0.75rem;">📊 Key Metrics</h4>
                            <div style="background: #f8fafc; padding: 1rem; border-radius: 8px;">
                                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem;">
                                    <div><strong>{len(df[df['lead_company'] == company_id])}</strong> Leading</div>
                                    <div><strong>{len(company_uc)}</strong> Total Involved</div>
                                    <div><strong>{len(company_uc[company_uc['status'] == 'In Progress'])}</strong> In Progress</div>
                                    <div><strong>{company_uc['progress'].mean():.0f}%</strong> Avg Progress</div>
                                </div>
                            </div>
                        </div>
                        
                        <div>
                            <h4 style="color: {color}; margin-bottom: 0.75rem;">👤 Primary Contact</h4>
                            <div style="background: #f8fafc; padding: 1rem; border-radius: 8px;">
                                {f"<strong>{primary_contact['name']}</strong><br>{primary_contact['role']}<br>📧 {primary_contact['email']}" if primary_contact is not None else "No primary contact assigned"}
                            </div>
                        </div>
                    </div>
                    
                    <div style="margin-top: 1.5rem;">
                        <h4 style="color: {color}; margin-bottom: 0.75rem;">📋 Active Use Cases</h4>
                        <ul style="margin: 0; padding-left: 1.5rem;">
                            {"".join([f"<li><strong>{row['id']}</strong>: {row['title']} ({row['status']})</li>" for _, row in company_uc.head(5).iterrows()])}
                        </ul>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Download button
                st.download_button(
                    "📥 Download as PDF",
                    generate_one_pager(pager['type'], pager['selection'], st.session_state),
                    file_name=f"one_pager_{company_id}_{datetime.now().strftime('%Y%m%d')}.html",
                    mime="text/html"
                )


def render_governance():
    """Render the three-tier governance structure view."""
    st.markdown("### 🏛️ Governance Structure")
    st.caption("Three-tiered organizational framework for DDPA × Snowflake collaboration")
    
    # Overview metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card" style="border-left: 4px solid #dc2626;">
            <div class="metric-value" style="font-size: 1.5rem; color: #dc2626;">Operations</div>
            <div class="metric-label">Work Group</div>
            <div style="margin-top: 0.5rem; font-size: 0.8rem; color: #64748b;">
                {len(GOVERNANCE_TIERS['operations_work_group']['members'])} Members | Monthly→Quarterly
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card" style="border-left: 4px solid #0066B1;">
            <div class="metric-value" style="font-size: 1.5rem; color: #0066B1;">Steering</div>
            <div class="metric-label">Committee</div>
            <div style="margin-top: 0.5rem; font-size: 0.8rem; color: #64748b;">
                {len(GOVERNANCE_TIERS['steering_committee']['members'])} Members | Monthly
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card" style="border-left: 4px solid #16a34a;">
            <div class="metric-value" style="font-size: 1.5rem; color: #16a34a;">User</div>
            <div class="metric-label">Community</div>
            <div style="margin-top: 0.5rem; font-size: 0.8rem; color: #64748b;">
                All Members | Bi-Monthly Workshops
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Detailed tier information
    for tier_key, tier in GOVERNANCE_TIERS.items():
        color = "#dc2626" if "operations" in tier_key else "#0066B1" if "steering" in tier_key else "#16a34a"
        
        with st.expander(f"**{tier['name']}**", expanded=True):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Description:** {tier['description']}")
                st.markdown(f"**Meeting Cadence:** {tier['cadence']}")
                
                st.markdown("**Responsibilities:**")
                for resp in tier['responsibilities']:
                    st.markdown(f"- {resp}")
            
            with col2:
                st.markdown("**Members:**")
                members_str = tier['members']
                if members_str == ["ALL"]:
                    st.markdown("All member companies + partners")
                else:
                    for member in members_str:
                        member_name = get_company_name(member) if member not in ["DDPA", "SNOWFLAKE"] else member
                        st.markdown(f"• {member_name}")
    
    # Onboarding Status
    st.markdown("---")
    st.markdown("#### 🚀 Member Company Onboarding Status")
    
    # Initialize onboarding in session state if not exists
    if 'onboarding' not in st.session_state:
        onboarding_data = []
        for company_id, status in ONBOARDING_STATUS.items():
            company_name = get_company_name(company_id)
            onboarding_data.append({
                "company_id": company_id,
                "company": company_name,
                "status": status["status"],
                "phase": status["phase"],
                "onboarded_date": status["onboarded_date"] or ""
            })
        st.session_state.onboarding = pd.DataFrame(onboarding_data)
    
    # Editable onboarding status
    onboarding_tabs = st.tabs(["📊 View Status", "✏️ Edit Status"])
    
    with onboarding_tabs[0]:
        # Display styled view
        for _, row in st.session_state.onboarding.iterrows():
            status_color = "#16a34a" if row['status'] == "Active" else "#f59e0b" if row['status'] == "Onboarding" else "#3b82f6"
            st.markdown(f"""
            <div style="background: white; border-left: 4px solid {status_color}; border-radius: 0 8px 8px 0; padding: 0.75rem 1rem; margin-bottom: 0.5rem;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <strong>{row['company']}</strong>
                    <div>
                        <span style="background: {status_color}20; color: {status_color}; padding: 0.2rem 0.5rem; border-radius: 4px; font-size: 0.8rem; margin-right: 0.5rem;">{row['status']}</span>
                        <span style="background: #f1f5f9; padding: 0.2rem 0.5rem; border-radius: 4px; font-size: 0.8rem;">{row['phase']}</span>
                    </div>
                </div>
                <div style="font-size: 0.8rem; color: #64748b; margin-top: 0.25rem;">
                    {f"Onboarded: {row['onboarded_date']}" if row['onboarded_date'] else "Pending onboarding"}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with onboarding_tabs[1]:
        st.info("💡 Edit onboarding status directly. Changes are saved when you click 'Save'.")
        
        edited_onboarding = st.data_editor(
            st.session_state.onboarding,
            use_container_width=True,
            hide_index=True,
            column_config={
                "company_id": st.column_config.TextColumn("ID", disabled=True, width="small"),
                "company": st.column_config.TextColumn("Company", disabled=True, width="medium"),
                "status": st.column_config.SelectboxColumn(
                    "Status",
                    options=["Active", "Onboarding", "Evaluating", "Pending"],
                    required=True
                ),
                "phase": st.column_config.SelectboxColumn(
                    "Phase",
                    options=[
                        "Full Production",
                        "Phase 2 - Expansion",
                        "Phase 1 - Pilot",
                        "Technical Evaluation",
                        "Initial Discussions"
                    ],
                    required=True
                ),
                "onboarded_date": st.column_config.TextColumn("Onboarded Date", help="Format: YYYY-MM-DD")
            },
            key="onboarding_editor"
        )
        
        if st.button("💾 Save Onboarding Status", type="primary"):
            st.session_state.onboarding = edited_onboarding
            st.success("✅ Onboarding status saved!")
    
    # Partners
    st.markdown("---")
    st.markdown("#### 🤝 Partners & RSAs")
    
    # Initialize partners in session state if not exists
    if 'partners' not in st.session_state:
        st.session_state.partners = pd.DataFrame(PARTNERS)
    
    partner_tabs = st.tabs(["📊 View Partners", "✏️ Edit Partners"])
    
    with partner_tabs[0]:
        for _, partner in st.session_state.partners.iterrows():
            status_color = "#16a34a" if partner['engagement_status'] == "Active" else "#f59e0b" if partner['engagement_status'] == "On-call" else "#3b82f6"
            st.markdown(f"""
            <div style="background: white; border: 1px solid #e2e8f0; border-radius: 8px; padding: 1rem; margin-bottom: 0.5rem;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong>{partner['name']}</strong> 
                        <span style="background: #f1f5f9; padding: 0.2rem 0.5rem; border-radius: 4px; font-size: 0.75rem; margin-left: 0.5rem;">{partner['type']}</span>
                    </div>
                    <span style="background: {status_color}20; color: {status_color}; padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.8rem;">{partner['engagement_status']}</span>
                </div>
                <div style="font-size: 0.85rem; color: #64748b; margin-top: 0.5rem;">
                    Specialty: {partner['specialty']} | Contact: {partner['contact']} ({partner['email']})
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with partner_tabs[1]:
        st.info("💡 Edit partner information directly. Add new partners using the button below.")
        
        # Add new partner button
        if st.button("➕ Add New Partner"):
            new_partner = {
                "id": f"P{len(st.session_state.partners) + 1:03d}",
                "name": "New Partner",
                "type": "RSA",
                "specialty": "General",
                "contact": "Contact Name",
                "email": "partner@company.com",
                "engagement_status": "Evaluating"
            }
            st.session_state.partners = pd.concat([
                st.session_state.partners,
                pd.DataFrame([new_partner])
            ], ignore_index=True)
            st.rerun()
        
        edited_partners = st.data_editor(
            st.session_state.partners,
            use_container_width=True,
            hide_index=True,
            num_rows="dynamic",
            column_config={
                "id": st.column_config.TextColumn("ID", disabled=True, width="small"),
                "name": st.column_config.TextColumn("Partner Name", width="medium"),
                "type": st.column_config.SelectboxColumn(
                    "Type",
                    options=["RSA", "ISV", "Consulting", "Technology"],
                    required=True
                ),
                "specialty": st.column_config.TextColumn("Specialty"),
                "contact": st.column_config.TextColumn("Contact Name"),
                "email": st.column_config.TextColumn("Email"),
                "engagement_status": st.column_config.SelectboxColumn(
                    "Status",
                    options=["Active", "On-call", "Evaluating", "Inactive"],
                    required=True
                )
            },
            key="partners_editor"
        )
        
        if st.button("💾 Save Partner Data", type="primary"):
            st.session_state.partners = edited_partners
            st.success("✅ Partner data saved!")


def render_financial_tracking():
    """Render financial tracking dashboard."""
    st.markdown("### 💰 Financial Tracking")
    st.caption("Monitor $15M commitment, spend by member company, and investment allocations")
    
    # Load financial data
    spend_df = get_monthly_spend()
    investments_df = get_investment_allocations()
    drawdowns_df = get_marketplace_drawdowns()
    
    # Calculate totals
    total_spent = spend_df[[c for c in spend_df.columns if c != 'month']].sum().sum() * 1000
    total_commitment = FINANCIAL_DATA['total_commitment']
    remaining = total_commitment - total_spent
    pct_used = (total_spent / total_commitment) * 100
    
    training_spent = investments_df[investments_df['category'] == 'Training']['amount'].sum()
    training_budget = FINANCIAL_DATA['training_budget']
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">${total_commitment/1000000:.0f}M</div>
            <div class="metric-label">Total Commitment</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: #16a34a;">${total_spent/1000000:.1f}M</div>
            <div class="metric-label">Spent to Date ({pct_used:.1f}%)</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: #0066B1;">${remaining/1000000:.1f}M</div>
            <div class="metric-label">Remaining</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: #7c3aed;">${training_budget/1000:.0f}K</div>
            <div class="metric-label">Training Budget</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Tabs for different financial views
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Spend by Company", 
        "💵 Investment Allocations", 
        "🏪 Marketplace Drawdowns", 
        "📊 Budget Summary",
        "✏️ Edit Financial Data"
    ])
    
    with tab1:
        st.markdown("#### Monthly Snowflake Spend by Member Company")
        
        # Prepare data for stacked area chart
        spend_melted = spend_df.melt(id_vars=['month'], var_name='Company', value_name='Spend ($K)')
        spend_melted['Company'] = spend_melted['Company'].apply(get_company_name)
        
        fig = px.area(
            spend_melted,
            x='month',
            y='Spend ($K)',
            color='Company',
            title="Monthly Snowflake Spend Trend"
        )
        fig.update_layout(
            xaxis_title="Month",
            yaxis_title="Spend ($K)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02),
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Company breakdown table
        st.markdown("#### Spend by Company (YTD)")
        company_totals = spend_df[[c for c in spend_df.columns if c != 'month']].sum()
        company_totals_df = pd.DataFrame({
            'Company': [get_company_name(c) for c in company_totals.index],
            'Total Spend ($K)': company_totals.values,
            'Avg Monthly ($K)': (company_totals.values / len(spend_df)).round(1),
            '% of Total': ((company_totals.values / company_totals.sum()) * 100).round(1)
        })
        st.dataframe(company_totals_df, use_container_width=True, hide_index=True)
    
    with tab2:
        st.markdown("#### Investment & Training Allocations ($350K Budget)")
        
        # Progress bar
        training_pct = (training_spent / training_budget) * 100
        st.markdown(f"""
        <div style="margin-bottom: 1rem;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span>Training Budget Used</span>
                <span>${training_spent/1000:.0f}K / ${training_budget/1000:.0f}K ({training_pct:.0f}%)</span>
            </div>
            <div class="progress-container">
                <div class="progress-bar" style="width: {training_pct}%; background: linear-gradient(90deg, #16a34a, #22c55e);"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Investment table
        for _, inv in investments_df.iterrows():
            status_color = "#16a34a" if inv['status'] == "Completed" else "#3b82f6" if inv['status'] == "In Progress" else "#94a3b8"
            cat_icon = "🎓" if inv['category'] == "Training" else "🤝" if inv['category'] == "Partner" else "📁"
            
            st.markdown(f"""
            <div style="background: white; border: 1px solid #e2e8f0; border-radius: 8px; padding: 1rem; margin-bottom: 0.5rem;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span>{cat_icon}</span>
                        <strong style="margin-left: 0.5rem;">{inv['description']}</strong>
                        <span style="background: #f1f5f9; padding: 0.2rem 0.5rem; border-radius: 4px; font-size: 0.75rem; margin-left: 0.5rem;">{inv['category']}</span>
                    </div>
                    <div style="text-align: right;">
                        <strong style="color: #0066B1;">${inv['amount']:,}</strong>
                        <span style="background: {status_color}20; color: {status_color}; padding: 0.2rem 0.5rem; border-radius: 4px; font-size: 0.75rem; margin-left: 0.5rem;">{inv['status']}</span>
                    </div>
                </div>
                <div style="font-size: 0.8rem; color: #64748b; margin-top: 0.5rem;">
                    Beneficiary: {inv['beneficiary']} | Date: {inv['date']}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("#### Marketplace Capacity Drawdowns & Billback")
        
        total_drawdown = drawdowns_df['amount'].sum()
        pending_billback = drawdowns_df[drawdowns_df['billback_status'] == 'Pending']['amount'].sum()
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Drawdowns", f"${total_drawdown:,}")
        col2.metric("Pending Billback", f"${pending_billback:,}")
        col3.metric("Completed", f"${total_drawdown - pending_billback:,}")
        
        st.dataframe(
            drawdowns_df.assign(
                company=drawdowns_df['company'].apply(get_company_name)
            ).rename(columns={
                'company': 'Company',
                'product': 'Product',
                'amount': 'Amount ($)',
                'date': 'Date',
                'billback_status': 'Billback Status'
            }),
            use_container_width=True,
            hide_index=True
        )
    
    with tab4:
        st.markdown("#### Budget Summary & Projections")
        
        # Pie chart of spend categories
        category_spend = investments_df.groupby('category')['amount'].sum().reset_index()
        
        fig = px.pie(
            category_spend,
            values='amount',
            names='category',
            title="Investment Allocation by Category",
            color_discrete_sequence=['#0066B1', '#29B5E8', '#00D4AA']
        )
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
        
        # Commitment tracking
        st.markdown("##### $15M Commitment Tracking")
        st.markdown(f"""
        - **Commitment Period:** {FINANCIAL_DATA['commitment_period']}
        - **Contracted Companies:** {len(FINANCIAL_DATA['contracted_companies'])} (CA, MA, NY, PA, TX, IL)
        - **Rollover Credits:** ${FINANCIAL_DATA['rollover_credits']:,}
        """)
    
    with tab5:
        st.markdown("#### ✏️ Edit Financial Data")
        st.info("💡 Edit spending data, investments, and drawdowns using the spreadsheet-like editors below.")
        
        edit_section = st.selectbox(
            "Select data to edit",
            ["Monthly Spend", "Investment Allocations", "Marketplace Drawdowns"]
        )
        
        if edit_section == "Monthly Spend":
            st.markdown("##### Edit Monthly Spend by Company ($K)")
            
            # Initialize spend data in session state if not exists
            if 'monthly_spend' not in st.session_state:
                st.session_state.monthly_spend = spend_df.copy()
            
            edited_spend = st.data_editor(
                st.session_state.monthly_spend,
                use_container_width=True,
                hide_index=True,
                num_rows="dynamic",
                column_config={
                    "month": st.column_config.TextColumn("Month", width="small"),
                    "CA": st.column_config.NumberColumn("California ($K)", min_value=0, step=1),
                    "MA": st.column_config.NumberColumn("Massachusetts ($K)", min_value=0, step=1),
                    "NY": st.column_config.NumberColumn("New York ($K)", min_value=0, step=1),
                    "PA": st.column_config.NumberColumn("Pennsylvania ($K)", min_value=0, step=1),
                    "TX": st.column_config.NumberColumn("Texas ($K)", min_value=0, step=1),
                    "IL": st.column_config.NumberColumn("Illinois ($K)", min_value=0, step=1)
                },
                key="spend_editor"
            )
            
            if st.button("💾 Save Spend Data", type="primary"):
                st.session_state.monthly_spend = edited_spend
                st.success("✅ Monthly spend data saved!")
        
        elif edit_section == "Investment Allocations":
            st.markdown("##### Edit Investment Allocations")
            
            # Initialize investments in session state if not exists
            if 'investments' not in st.session_state:
                st.session_state.investments = investments_df.copy()
            
            # Add new investment button
            if st.button("➕ Add New Investment"):
                new_inv = {
                    "id": f"INV{len(st.session_state.investments) + 1:03d}",
                    "category": "Training",
                    "description": "New Investment",
                    "amount": 0,
                    "beneficiary": "All",
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "status": "Planned"
                }
                st.session_state.investments = pd.concat([
                    st.session_state.investments,
                    pd.DataFrame([new_inv])
                ], ignore_index=True)
                st.rerun()
            
            edited_investments = st.data_editor(
                st.session_state.investments,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "id": st.column_config.TextColumn("ID", disabled=True, width="small"),
                    "category": st.column_config.SelectboxColumn(
                        "Category",
                        options=["Training", "Partner", "Project"],
                        required=True
                    ),
                    "description": st.column_config.TextColumn("Description", width="large"),
                    "amount": st.column_config.NumberColumn("Amount ($)", min_value=0, step=1000, format="$%d"),
                    "beneficiary": st.column_config.TextColumn("Beneficiary"),
                    "date": st.column_config.DateColumn("Date"),
                    "status": st.column_config.SelectboxColumn(
                        "Status",
                        options=["Planned", "In Progress", "Completed"],
                        required=True
                    )
                },
                key="investments_editor"
            )
            
            if st.button("💾 Save Investment Data", type="primary"):
                st.session_state.investments = edited_investments
                st.success("✅ Investment data saved!")
        
        else:  # Marketplace Drawdowns
            st.markdown("##### Edit Marketplace Drawdowns")
            
            # Initialize drawdowns in session state if not exists
            if 'drawdowns' not in st.session_state:
                st.session_state.drawdowns = drawdowns_df.copy()
            
            # Add new drawdown button
            if st.button("➕ Add New Drawdown"):
                new_dd = {
                    "id": f"DD{len(st.session_state.drawdowns) + 1:03d}",
                    "company": "CA",
                    "product": "New Product",
                    "amount": 0,
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "billback_status": "Pending"
                }
                st.session_state.drawdowns = pd.concat([
                    st.session_state.drawdowns,
                    pd.DataFrame([new_dd])
                ], ignore_index=True)
                st.rerun()
            
            edited_drawdowns = st.data_editor(
                st.session_state.drawdowns,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "id": st.column_config.TextColumn("ID", disabled=True, width="small"),
                    "company": st.column_config.SelectboxColumn(
                        "Company",
                        options=[c['id'] for c in MEMBER_COMPANIES],
                        required=True
                    ),
                    "product": st.column_config.TextColumn("Product"),
                    "amount": st.column_config.NumberColumn("Amount ($)", min_value=0, step=100, format="$%d"),
                    "date": st.column_config.DateColumn("Date"),
                    "billback_status": st.column_config.SelectboxColumn(
                        "Billback Status",
                        options=["Pending", "Completed", "Waived"],
                        required=True
                    )
                },
                key="drawdowns_editor"
            )
            
            if st.button("💾 Save Drawdown Data", type="primary"):
                st.session_state.drawdowns = edited_drawdowns
                st.success("✅ Drawdown data saved!")


def render_meetings():
    """Render meeting cadence management with editable capabilities."""
    st.markdown("### 📅 Meeting Cadence")
    st.caption("Track Operations Work Group, Steering Committee, and User Community meetings")
    
    # Initialize meetings in session state if not exists
    if 'meetings' not in st.session_state:
        st.session_state.meetings = get_scheduled_meetings()
    
    meetings_df = st.session_state.meetings
    
    # Upcoming meetings
    today = datetime.now().strftime("%Y-%m-%d")
    upcoming = meetings_df[meetings_df['date'] >= today].head(5)
    
    st.markdown("#### 📆 Upcoming Meetings")
    
    for _, meeting in upcoming.iterrows():
        tier_color = "#dc2626" if "Operations" in meeting['type'] else "#0066B1" if "Steering" in meeting['type'] else "#16a34a"
        
        st.markdown(f"""
        <div style="background: white; border-left: 4px solid {tier_color}; border-radius: 0 8px 8px 0; padding: 1rem; margin-bottom: 0.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <strong>{meeting['type']}</strong>
                    <span style="color: #64748b; margin-left: 1rem;">👥 {meeting['attendees_expected']} expected</span>
                </div>
                <span style="background: #f1f5f9; padding: 0.25rem 0.75rem; border-radius: 4px; font-weight: 500;">
                    {meeting['date']}
                </span>
            </div>
            <div style="font-size: 0.85rem; color: #64748b; margin-top: 0.5rem;">
                {meeting['notes']}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Meeting calendar by tier
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔴 Operations Work Group", 
        "🔵 Steering Committee", 
        "🟢 User Community",
        "✏️ Manage Meetings"
    ])
    
    with tab1:
        ops_meetings = meetings_df[meetings_df['tier'] == 'operations_work_group']
        st.markdown(f"**Cadence:** Monthly (transitioning to Quarterly)")
        st.markdown(f"**Total Meetings:** {len(ops_meetings)} scheduled for 2024")
        st.dataframe(
            ops_meetings[['date', 'status', 'attendees_expected', 'notes']].rename(columns={
                'date': 'Date', 'status': 'Status', 'attendees_expected': 'Expected Attendees', 'notes': 'Notes'
            }),
            use_container_width=True,
            hide_index=True
        )
    
    with tab2:
        sc_meetings = meetings_df[meetings_df['tier'] == 'steering_committee']
        st.markdown(f"**Cadence:** Monthly")
        st.markdown(f"**Total Meetings:** {len(sc_meetings)} scheduled for 2024")
        st.dataframe(
            sc_meetings[['date', 'status', 'attendees_expected', 'notes']].rename(columns={
                'date': 'Date', 'status': 'Status', 'attendees_expected': 'Expected Attendees', 'notes': 'Notes'
            }),
            use_container_width=True,
            hide_index=True
        )
    
    with tab3:
        uc_meetings = meetings_df[meetings_df['tier'] == 'user_community']
        st.markdown(f"**Cadence:** Bi-Monthly Workshops")
        st.markdown(f"**Total Workshops:** {len(uc_meetings)} scheduled for 2024")
        st.dataframe(
            uc_meetings[['date', 'status', 'attendees_expected', 'notes']].rename(columns={
                'date': 'Date', 'status': 'Status', 'attendees_expected': 'Expected Attendees', 'notes': 'Workshop Topic'
            }),
            use_container_width=True,
            hide_index=True
        )
    
    with tab4:
        st.markdown("#### ✏️ Manage Meetings")
        st.info("💡 Add new meetings or edit existing ones using the forms below.")
        
        # Add new meeting form
        with st.expander("➕ Add New Meeting", expanded=False):
            with st.form("add_meeting_form"):
                col1, col2 = st.columns(2)
                with col1:
                    meeting_tier = st.selectbox(
                        "Meeting Tier*",
                        options=['operations_work_group', 'steering_committee', 'user_community'],
                        format_func=lambda x: {
                            'operations_work_group': '🔴 Operations Work Group',
                            'steering_committee': '🔵 Steering Committee',
                            'user_community': '🟢 User Community'
                        }.get(x, x)
                    )
                    meeting_date = st.date_input("Meeting Date*", value=datetime.now())
                with col2:
                    meeting_type = st.text_input(
                        "Meeting Type*",
                        placeholder="e.g., Monthly Sync, Quarterly Review, Workshop"
                    )
                    attendees = st.number_input("Expected Attendees", min_value=1, value=10)
                
                meeting_status = st.selectbox("Status", ["Scheduled", "Completed", "Cancelled"])
                meeting_notes = st.text_area("Notes/Agenda", placeholder="Meeting agenda or notes...")
                
                if st.form_submit_button("➕ Add Meeting", type="primary", use_container_width=True):
                    new_meeting = {
                        "id": f"MTG{len(st.session_state.meetings) + 1:03d}",
                        "tier": meeting_tier,
                        "type": meeting_type,
                        "date": meeting_date.strftime("%Y-%m-%d"),
                        "status": meeting_status,
                        "attendees_expected": attendees,
                        "notes": meeting_notes
                    }
                    st.session_state.meetings = pd.concat([
                        st.session_state.meetings,
                        pd.DataFrame([new_meeting])
                    ], ignore_index=True)
                    st.success(f"✅ Meeting '{meeting_type}' scheduled for {meeting_date}!")
                    st.rerun()
        
        st.markdown("---")
        st.markdown("##### Edit All Meetings")
        
        # Editable meetings grid
        edited_meetings = st.data_editor(
            st.session_state.meetings,
            use_container_width=True,
            hide_index=True,
            num_rows="dynamic",
            column_config={
                "id": st.column_config.TextColumn("ID", disabled=True, width="small"),
                "tier": st.column_config.SelectboxColumn(
                    "Tier",
                    options=['operations_work_group', 'steering_committee', 'user_community'],
                    required=True,
                    width="medium"
                ),
                "type": st.column_config.TextColumn("Meeting Type", width="medium"),
                "date": st.column_config.DateColumn("Date", required=True),
                "status": st.column_config.SelectboxColumn(
                    "Status",
                    options=["Scheduled", "Completed", "Cancelled"],
                    required=True,
                    width="small"
                ),
                "attendees_expected": st.column_config.NumberColumn(
                    "Attendees",
                    min_value=1,
                    step=1,
                    width="small"
                ),
                "notes": st.column_config.TextColumn("Notes/Agenda", width="large")
            },
            key="meetings_editor"
        )
        
        if st.button("💾 Save All Meeting Changes", type="primary"):
            st.session_state.meetings = edited_meetings
            st.success("✅ Meeting data saved!")
    
    # JIRA Integration placeholder
    st.markdown("---")
    st.markdown("#### 🔗 External Integrations")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div style="background: #f8fafc; border: 1px dashed #cbd5e1; border-radius: 8px; padding: 1.5rem; text-align: center;">
            <div style="font-size: 2rem;">📋</div>
            <strong>JIRA</strong>
            <div style="font-size: 0.8rem; color: #64748b; margin-top: 0.5rem;">Connect to local JIRA for detailed task management</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Configure JIRA", key="jira_btn"):
            st.info("JIRA integration configuration coming soon")
    
    with col2:
        st.markdown("""
        <div style="background: #f8fafc; border: 1px dashed #cbd5e1; border-radius: 8px; padding: 1.5rem; text-align: center;">
            <div style="font-size: 2rem;">📆</div>
            <strong>Calendar</strong>
            <div style="font-size: 0.8rem; color: #64748b; margin-top: 0.5rem;">Sync with Google/Outlook calendars</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Configure Calendar", key="cal_btn"):
            st.info("Calendar sync configuration coming soon")
    
    with col3:
        st.markdown("""
        <div style="background: #f8fafc; border: 1px dashed #cbd5e1; border-radius: 8px; padding: 1.5rem; text-align: center;">
            <div style="font-size: 2rem;">📧</div>
            <strong>Email</strong>
            <div style="font-size: 0.8rem; color: #64748b; margin-top: 0.5rem;">Automated meeting reminders</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Configure Email", key="email_btn"):
            st.info("Email notification configuration coming soon")


def render_settings():
    """Render settings view."""
    st.markdown("### ⚙️ Settings & Configuration")
    
    tab1, tab2, tab3, tab4 = st.tabs(["🎨 Appearance", "🔗 Integrations", "👤 Access Control", "📊 Data Management"])
    
    with tab1:
        st.markdown("#### Theme & Branding")
        
        col1, col2 = st.columns(2)
        with col1:
            st.color_picker("Primary Color", "#0066B1")
            st.selectbox("Logo Display", ["DDPA × Snowflake", "DDPA Only", "Snowflake Only"])
        with col2:
            st.selectbox("Theme", ["Light", "Dark", "System"])
            st.selectbox("Font", ["Plus Jakarta Sans", "Inter", "SF Pro"])
    
    with tab2:
        st.markdown("#### Data Source Connections")
        
        with st.expander("❄️ Snowflake Connection", expanded=True):
            st.text_input("Account", placeholder="org-account")
            st.text_input("Warehouse", placeholder="COMPUTE_WH")
            st.text_input("Database", placeholder="DDPA_PROJECT_TRACKER")
            st.text_input("Schema", placeholder="PUBLIC")
            if st.button("Test Connection"):
                st.success("✅ Connection successful!")
        
        with st.expander("📊 Export Settings"):
            st.checkbox("Auto-sync to Snowflake", value=True)
            st.number_input("Sync interval (minutes)", value=30, min_value=5)
    
    with tab3:
        st.markdown("#### Role-Based Access Control")
        st.caption("Configure different access levels for stakeholder groups")
        
        st.markdown("""
        <div style="background: #fef3c7; border: 1px solid #f59e0b; border-radius: 8px; padding: 1rem; margin-bottom: 1rem;">
            <strong>⚠️ Access Control Configuration</strong><br>
            <span style="font-size: 0.9rem;">Role-based access will be enforced when connected to Snowflake authentication.</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Role definitions
        roles = {
            "Executive": {
                "description": "Full access to all dashboards and data",
                "permissions": ["Dashboard", "Governance", "Financial Tracking", "All Use Cases", "Reports"],
                "members": ["Matt Johnson", "Sarah Chen", "Robert Martinez"]
            },
            "Steering Committee": {
                "description": "Strategic oversight access",
                "permissions": ["Dashboard", "Governance", "Use Cases", "Roadmap", "Duplicate Detection"],
                "members": ["All primary contacts"]
            },
            "Operations": {
                "description": "Day-to-day operations access",
                "permissions": ["Dashboard", "Use Cases (own company)", "Roadmap", "Contacts"],
                "members": ["All company members"]
            },
            "User Community": {
                "description": "Read-only access to shared resources",
                "permissions": ["Dashboard (limited)", "Roadmap (view only)", "Meeting Schedule"],
                "members": ["All registered users"]
            },
            "External Partner": {
                "description": "Limited access for partners like RSAs",
                "permissions": ["Assigned Projects", "Meeting Schedule"],
                "members": ["Partner contacts"]
            }
        }
        
        for role_name, role_info in roles.items():
            with st.expander(f"👤 {role_name}"):
                st.markdown(f"**Description:** {role_info['description']}")
                st.markdown("**Permissions:**")
                for perm in role_info['permissions']:
                    st.markdown(f"- ✅ {perm}")
                st.markdown(f"**Members:** {', '.join(role_info['members']) if isinstance(role_info['members'], list) else role_info['members']}")
    
    with tab4:
        st.markdown("#### Data Management")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📥 Export All Data", use_container_width=True):
                st.success("Data exported successfully!")
            if st.button("🔄 Reset to Sample Data", use_container_width=True):
                st.session_state.use_cases = get_sample_use_cases()
                st.session_state.contacts = get_sample_contacts()
                st.session_state.meetings = get_sample_meetings()
                st.success("Reset to sample data!")
                st.rerun()
        with col2:
            if st.button("📤 Import Data", use_container_width=True):
                st.info("Upload functionality would appear here")
            if st.button("🗑️ Clear All Data", use_container_width=True):
                st.warning("This would clear all data")


def render_footer():
    """Render the footer with co-branding."""
    dd_logo_base64 = get_logo_base64()
    snow_logo_base64, snow_logo_type = get_snowflake_logo_base64()
    snow_icon_base64 = get_snowflake_icon_base64()
    
    delta_logo_html = f'<img src="data:image/webp;base64,{dd_logo_base64}" style="height: 35px; background: white; padding: 4px; border-radius: 6px;">' if dd_logo_base64 else '<span style="color: #39B54A; font-weight: bold;">Delta Dental</span>'
    
    # Use the full Snowflake logo for footer
    if snow_logo_base64:
        snowflake_html = f'<img src="data:image/{snow_logo_type};base64,{snow_logo_base64}" style="height: 30px;">'
    elif snow_icon_base64:
        snowflake_html = f'<img src="data:image/png;base64,{snow_icon_base64}" style="height: 28px;"><span style="color: #29B5E8; font-weight: 600; margin-left: 4px;">Snowflake</span>'
    else:
        snowflake_html = '<span style="color: #29B5E8; font-weight: 600;">❄️ Snowflake</span>'
    
    st.markdown("---")
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; padding: 1rem 0; color: #64748b; font-size: 0.85rem; flex-wrap: wrap; gap: 1rem;">
        <div style="display: flex; align-items: center; gap: 1rem;">
            {delta_logo_html}
            <span style="color: #cbd5e1; font-size: 1.5rem;">×</span>
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                {snowflake_html}
            </div>
        </div>
        <div>
            © {datetime.now().year} DDPA × Snowflake Partnership | Project Planning Tracker
        </div>
    </div>
    """, unsafe_allow_html=True)


def main():
    """Main application entry point."""
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
    elif view == "Duplicate Detection":
        render_duplicate_detection()
    elif view == "One-Pagers":
        render_one_pagers()
    elif view == "Settings":
        render_settings()
    
    # Render footer with co-branding
    render_footer()


if __name__ == "__main__":
    main()
