"""
Sample data for Delta Dental Project Planning Tracker
This module provides initial data structures and sample data for the application.
"""

import pandas as pd
from datetime import datetime, timedelta
import random

# Member Companies
MEMBER_COMPANIES = [
    {"id": "CA", "name": "Delta Dental of California", "abbrev": "DDCA", "region": "West", "color": "#1E88E5"},
    {"id": "MA", "name": "Delta Dental of Massachusetts", "abbrev": "DDMA", "region": "Northeast", "color": "#43A047"},
    {"id": "HI", "name": "Delta Dental of Hawaii", "abbrev": "DDHI", "region": "West", "color": "#E53935"},
    {"id": "NY", "name": "Delta Dental of New York", "abbrev": "DDNY", "region": "Northeast", "color": "#8E24AA"},
    {"id": "PA", "name": "Delta Dental of Pennsylvania", "abbrev": "DDPA", "region": "Northeast", "color": "#FB8C00"},
    {"id": "TX", "name": "Delta Dental of Texas", "abbrev": "DDTX", "region": "South", "color": "#00ACC1"},
    {"id": "IL", "name": "Delta Dental of Illinois", "abbrev": "DDIL", "region": "Midwest", "color": "#5E35B1"},
    {"id": "WA", "name": "Delta Dental of Washington", "abbrev": "DDWA", "region": "West", "color": "#F4511E"},
]

# Priority Levels
PRIORITIES = ["P0 - Critical", "P1 - High", "P2 - Medium", "P3 - Low"]

# Status Options
STATUSES = ["Not Started", "Discovery", "In Progress", "On Hold", "Completed", "Cancelled"]

# Use Case Categories
CATEGORIES = [
    "Data Analytics & BI",
    "Machine Learning & AI",
    "Data Sharing & Collaboration",
    "Claims Processing",
    "Member Experience",
    "Provider Network",
    "Fraud Detection",
    "Regulatory Compliance",
    "Data Platform & Infrastructure",
    "Cost Optimization"
]

# Subcommittees (Legacy - kept for backward compatibility)
SUBCOMMITTEES = [
    "Data Governance",
    "Analytics & Insights",
    "Technology & Infrastructure",
    "Security & Compliance",
    "Member Experience",
    "Provider Relations"
]

# Three-Tiered Governance Structure
GOVERNANCE_TIERS = {
    "operations_work_group": {
        "name": "Umbrella Deal Operations Work Group",
        "description": "Monitor Snowflake spend, provide direction on investment spend, and general oversight",
        "cadence": "Monthly (moving to Quarterly)",
        "members": ["DDPA", "CA", "MA", "NY", "PA", "TX", "IL"],  # DDPA + 6 contracted MCs
        "responsibilities": [
            "Monitor aggregate Snowflake spend across member companies",
            "Provide direction on investment spend allocation",
            "General oversight of Snowflake partnership",
            "Approve major initiatives and budget allocations"
        ]
    },
    "steering_committee": {
        "name": "Snowflake Steering Committee", 
        "description": "Provide strategic oversight and guidance to all member companies leveraging Snowflake",
        "cadence": "Monthly",
        "members": ["DDPA", "CA", "MA", "NY", "PA", "TX", "IL", "HI", "WA", "SNOWFLAKE"],
        "responsibilities": [
            "Strategic oversight of all Snowflake initiatives",
            "Use case prioritization and validation",
            "Resource allocation decisions",
            "Cross-company collaboration coordination",
            "Partner engagement oversight"
        ]
    },
    "user_community": {
        "name": "Snowflake User Community",
        "description": "Ongoing education, hands-on labs, workshops aligned to member company priorities",
        "cadence": "Monthly/Bi-Monthly",
        "members": ["ALL"],
        "responsibilities": [
            "Technical training and enablement",
            "Hands-on labs and workshops",
            "Best practices sharing",
            "User community building",
            "Skills development"
        ]
    }
}

# Financial Commitment Tracking
FINANCIAL_DATA = {
    "total_commitment": 15000000,  # $15M total commitment
    "commitment_period": "2024-2026",
    "training_budget": 350000,  # $350K training funds
    "rollover_credits": 0,  # Updated monthly
    "contracted_companies": ["CA", "MA", "NY", "PA", "TX", "IL"],  # 6 contracted MCs
}

# Member Company Onboarding Status
ONBOARDING_STATUS = {
    "CA": {"status": "Active", "onboarded_date": "2023-01-01", "phase": "Production"},
    "MA": {"status": "Active", "onboarded_date": "2023-03-01", "phase": "Production"},
    "NY": {"status": "Active", "onboarded_date": "2023-06-01", "phase": "Production"},
    "PA": {"status": "Active", "onboarded_date": "2023-06-01", "phase": "Production"},
    "TX": {"status": "Active", "onboarded_date": "2023-09-01", "phase": "Production"},
    "IL": {"status": "Active", "onboarded_date": "2023-12-01", "phase": "Production"},
    "HI": {"status": "Onboarding", "onboarded_date": None, "phase": "Integration"},
    "WA": {"status": "Evaluating", "onboarded_date": None, "phase": "Discovery"},
}

# Sample Use Cases
def get_sample_use_cases():
    use_cases = [
        {
            "id": "UC001",
            "title": "Claims Fraud Detection using ML",
            "description": "Implement machine learning models to detect fraudulent claims patterns across member companies",
            "category": "Fraud Detection",
            "priority": "P0 - Critical",
            "status": "In Progress",
            "lead_company": "CA",
            "participating_companies": ["CA", "MA", "TX"],
            "start_date": "2024-01-15",
            "target_date": "2024-06-30",
            "progress": 45,
            "estimated_value": "$2.5M",
            "tags": ["ML", "Fraud", "Claims"],
            "subcommittee": "Analytics & Insights"
        },
        {
            "id": "UC002",
            "title": "Unified Member 360 Dashboard",
            "description": "Create a comprehensive member view combining data from all touchpoints",
            "category": "Member Experience",
            "priority": "P1 - High",
            "status": "Discovery",
            "lead_company": "MA",
            "participating_companies": ["MA", "NY", "PA"],
            "start_date": "2024-02-01",
            "target_date": "2024-08-31",
            "progress": 20,
            "estimated_value": "$1.8M",
            "tags": ["Dashboard", "Member", "360 View"],
            "subcommittee": "Member Experience"
        },
        {
            "id": "UC003",
            "title": "Provider Network Optimization",
            "description": "Analyze provider network data to optimize coverage and reduce gaps",
            "category": "Provider Network",
            "priority": "P1 - High",
            "status": "In Progress",
            "lead_company": "TX",
            "participating_companies": ["TX", "CA", "IL"],
            "start_date": "2024-01-01",
            "target_date": "2024-05-15",
            "progress": 65,
            "estimated_value": "$3.2M",
            "tags": ["Provider", "Network", "Optimization"],
            "subcommittee": "Provider Relations"
        },
        {
            "id": "UC004",
            "title": "Real-time Claims Processing",
            "description": "Implement streaming data pipeline for real-time claims adjudication",
            "category": "Claims Processing",
            "priority": "P0 - Critical",
            "status": "In Progress",
            "lead_company": "CA",
            "participating_companies": ["CA", "WA", "HI"],
            "start_date": "2024-03-01",
            "target_date": "2024-09-30",
            "progress": 30,
            "estimated_value": "$4.1M",
            "tags": ["Real-time", "Streaming", "Claims"],
            "subcommittee": "Technology & Infrastructure"
        },
        {
            "id": "UC005",
            "title": "Cross-Company Data Sharing Platform",
            "description": "Build secure data sharing infrastructure using Snowflake Data Clean Rooms",
            "category": "Data Sharing & Collaboration",
            "priority": "P1 - High",
            "status": "Discovery",
            "lead_company": "PA",
            "participating_companies": ["PA", "NY", "MA", "IL"],
            "start_date": "2024-04-01",
            "target_date": "2024-10-31",
            "progress": 15,
            "estimated_value": "$2.8M",
            "tags": ["Data Sharing", "Clean Rooms", "Collaboration"],
            "subcommittee": "Data Governance"
        },
        {
            "id": "UC006",
            "title": "Regulatory Compliance Reporting",
            "description": "Automated compliance reporting for state and federal regulations",
            "category": "Regulatory Compliance",
            "priority": "P2 - Medium",
            "status": "Not Started",
            "lead_company": "NY",
            "participating_companies": ["NY", "CA", "TX"],
            "start_date": "2024-05-01",
            "target_date": "2024-11-30",
            "progress": 0,
            "estimated_value": "$1.2M",
            "tags": ["Compliance", "Regulatory", "Automation"],
            "subcommittee": "Security & Compliance"
        },
        {
            "id": "UC007",
            "title": "Predictive Member Churn Analysis",
            "description": "ML model to predict member churn and enable proactive retention",
            "category": "Machine Learning & AI",
            "priority": "P2 - Medium",
            "status": "Discovery",
            "lead_company": "IL",
            "participating_companies": ["IL", "MA", "PA"],
            "start_date": "2024-06-01",
            "target_date": "2024-12-31",
            "progress": 10,
            "estimated_value": "$1.5M",
            "tags": ["ML", "Churn", "Prediction"],
            "subcommittee": "Analytics & Insights"
        },
        {
            "id": "UC008",
            "title": "National Claims Data Warehouse",
            "description": "Centralized data warehouse for aggregated claims data across all member companies",
            "category": "Data Platform & Infrastructure",
            "priority": "P0 - Critical",
            "status": "In Progress",
            "lead_company": "CA",
            "participating_companies": ["CA", "MA", "TX", "NY", "PA", "IL", "HI", "WA"],
            "start_date": "2024-01-01",
            "target_date": "2024-07-31",
            "progress": 55,
            "estimated_value": "$5.5M",
            "tags": ["Data Warehouse", "National", "Infrastructure"],
            "subcommittee": "Technology & Infrastructure"
        },
        {
            "id": "UC009",
            "title": "Cost Transparency Analytics",
            "description": "Build cost transparency tools for members to understand healthcare costs",
            "category": "Cost Optimization",
            "priority": "P2 - Medium",
            "status": "Not Started",
            "lead_company": "HI",
            "participating_companies": ["HI", "WA", "CA"],
            "start_date": "2024-07-01",
            "target_date": "2025-01-31",
            "progress": 0,
            "estimated_value": "$900K",
            "tags": ["Transparency", "Cost", "Analytics"],
            "subcommittee": "Member Experience"
        },
        {
            "id": "UC010",
            "title": "AI-Powered Customer Service Bot",
            "description": "Deploy conversational AI for member support using Snowflake Cortex",
            "category": "Machine Learning & AI",
            "priority": "P1 - High",
            "status": "Discovery",
            "lead_company": "WA",
            "participating_companies": ["WA", "CA", "MA"],
            "start_date": "2024-04-15",
            "target_date": "2024-10-15",
            "progress": 25,
            "estimated_value": "$2.1M",
            "tags": ["AI", "Chatbot", "Cortex", "Customer Service"],
            "subcommittee": "Member Experience"
        },
        # Duplicate detection examples - similar use cases
        {
            "id": "UC011",
            "title": "Fraud Analytics Platform",
            "description": "Analytics platform for identifying and preventing claims fraud",
            "category": "Fraud Detection",
            "priority": "P1 - High",
            "status": "Discovery",
            "lead_company": "NY",
            "participating_companies": ["NY", "PA"],
            "start_date": "2024-03-15",
            "target_date": "2024-09-15",
            "progress": 15,
            "estimated_value": "$1.9M",
            "tags": ["Fraud", "Analytics", "Claims"],
            "subcommittee": "Analytics & Insights"
        },
        {
            "id": "UC012",
            "title": "Member Experience Dashboard",
            "description": "Dashboard showing member journey and experience metrics",
            "category": "Member Experience",
            "priority": "P2 - Medium",
            "status": "Not Started",
            "lead_company": "TX",
            "participating_companies": ["TX", "IL"],
            "start_date": "2024-05-01",
            "target_date": "2024-11-01",
            "progress": 0,
            "estimated_value": "$1.1M",
            "tags": ["Dashboard", "Member", "Experience"],
            "subcommittee": "Member Experience"
        },
    ]
    return pd.DataFrame(use_cases)


# Sample Contacts
def get_sample_contacts():
    contacts = [
        # California
        {"id": "C001", "name": "Sarah Chen", "role": "VP of Data & Analytics", "company": "CA", "email": "schen@deltadental.com", "phone": "(415) 555-0101", "is_primary": True, "subcommittees": ["Analytics & Insights", "Technology & Infrastructure"]},
        {"id": "C002", "name": "Michael Rodriguez", "role": "Director of Engineering", "company": "CA", "email": "mrodriguez@deltadental.com", "phone": "(415) 555-0102", "is_primary": False, "subcommittees": ["Technology & Infrastructure"]},
        
        # Massachusetts
        {"id": "C003", "name": "Emily Thompson", "role": "Chief Data Officer", "company": "MA", "email": "ethompson@deltadental.com", "phone": "(617) 555-0201", "is_primary": True, "subcommittees": ["Data Governance", "Analytics & Insights"]},
        {"id": "C004", "name": "David Park", "role": "Senior Data Scientist", "company": "MA", "email": "dpark@deltadental.com", "phone": "(617) 555-0202", "is_primary": False, "subcommittees": ["Analytics & Insights"]},
        
        # Hawaii
        {"id": "C005", "name": "Lisa Nakamura", "role": "Director of Technology", "company": "HI", "email": "lnakamura@deltadental.com", "phone": "(808) 555-0301", "is_primary": True, "subcommittees": ["Technology & Infrastructure", "Member Experience"]},
        
        # New York
        {"id": "C006", "name": "James Wilson", "role": "VP of Compliance", "company": "NY", "email": "jwilson@deltadental.com", "phone": "(212) 555-0401", "is_primary": True, "subcommittees": ["Security & Compliance", "Data Governance"]},
        {"id": "C007", "name": "Amanda Foster", "role": "Data Analytics Manager", "company": "NY", "email": "afoster@deltadental.com", "phone": "(212) 555-0402", "is_primary": False, "subcommittees": ["Analytics & Insights"]},
        
        # Pennsylvania
        {"id": "C008", "name": "Robert Martinez", "role": "Chief Technology Officer", "company": "PA", "email": "rmartinez@deltadental.com", "phone": "(215) 555-0501", "is_primary": True, "subcommittees": ["Technology & Infrastructure", "Data Governance"]},
        {"id": "C009", "name": "Jennifer Lee", "role": "Director of Data Governance", "company": "PA", "email": "jlee@deltadental.com", "phone": "(215) 555-0502", "is_primary": False, "subcommittees": ["Data Governance"]},
        
        # Texas
        {"id": "C010", "name": "Christopher Brown", "role": "VP of Provider Relations", "company": "TX", "email": "cbrown@deltadental.com", "phone": "(512) 555-0601", "is_primary": True, "subcommittees": ["Provider Relations"]},
        {"id": "C011", "name": "Michelle Garcia", "role": "Analytics Lead", "company": "TX", "email": "mgarcia@deltadental.com", "phone": "(512) 555-0602", "is_primary": False, "subcommittees": ["Analytics & Insights"]},
        
        # Illinois
        {"id": "C012", "name": "Daniel Kim", "role": "Director of Innovation", "company": "IL", "email": "dkim@deltadental.com", "phone": "(312) 555-0701", "is_primary": True, "subcommittees": ["Technology & Infrastructure", "Analytics & Insights"]},
        
        # Washington
        {"id": "C013", "name": "Rachel Adams", "role": "VP of Member Experience", "company": "WA", "email": "radams@deltadental.com", "phone": "(206) 555-0801", "is_primary": True, "subcommittees": ["Member Experience"]},
        {"id": "C014", "name": "Kevin Patel", "role": "AI/ML Lead", "company": "WA", "email": "kpatel@deltadental.com", "phone": "(206) 555-0802", "is_primary": False, "subcommittees": ["Analytics & Insights", "Technology & Infrastructure"]},
        
        # DDPA / Association
        {"id": "C015", "name": "Matt Johnson", "role": "Executive Director", "company": "ASSOC", "email": "mjohnson@ddpa.org", "phone": "(555) 555-0901", "is_primary": True, "subcommittees": ["Data Governance", "Technology & Infrastructure"]},
        {"id": "C016", "name": "Patricia Williams", "role": "Program Manager", "company": "ASSOC", "email": "pwilliams@ddpa.org", "phone": "(555) 555-0902", "is_primary": False, "subcommittees": ["Data Governance"]},
        
        # Snowflake
        {"id": "C017", "name": "Alex Turner", "role": "Solution Architect", "company": "SNOWFLAKE", "email": "aturner@snowflake.com", "phone": "(555) 555-1001", "is_primary": True, "subcommittees": ["Technology & Infrastructure"]},
        {"id": "C018", "name": "Sophia Nguyen", "role": "Account Executive", "company": "SNOWFLAKE", "email": "snguyen@snowflake.com", "phone": "(555) 555-1002", "is_primary": False, "subcommittees": []},
    ]
    return pd.DataFrame(contacts)


# Sample Meeting Notes
def get_sample_meetings():
    meetings = [
        {
            "id": "M001",
            "title": "Q1 Kickoff - National Data Platform",
            "date": "2024-01-15",
            "attendees": ["Sarah Chen", "Emily Thompson", "Matt Johnson", "Alex Turner"],
            "companies": ["CA", "MA", "ASSOC", "SNOWFLAKE"],
            "summary": "Aligned on Q1 priorities for national data platform. Agreed on phased rollout starting with CA and MA.",
            "action_items": ["Finalize architecture doc by 1/31", "Schedule deep dive with security team", "Set up shared Snowflake account"],
            "related_use_cases": ["UC008", "UC005"]
        },
        {
            "id": "M002",
            "title": "Fraud Detection Working Group",
            "date": "2024-02-01",
            "attendees": ["Sarah Chen", "Amanda Foster", "Michelle Garcia"],
            "companies": ["CA", "NY", "TX"],
            "summary": "Reviewed ML model approaches for fraud detection. Identified potential overlap with NY initiative.",
            "action_items": ["Consolidate CA and NY efforts", "Share model performance metrics", "Schedule follow-up in 2 weeks"],
            "related_use_cases": ["UC001", "UC011"]
        },
        {
            "id": "M003",
            "title": "Monthly Steering Committee",
            "date": "2024-02-15",
            "attendees": ["Matt Johnson", "Sarah Chen", "Robert Martinez", "James Wilson", "Alex Turner"],
            "companies": ["ASSOC", "CA", "PA", "NY", "SNOWFLAKE"],
            "summary": "Monthly review of all active initiatives. Reprioritized based on resource availability.",
            "action_items": ["Update roadmap by 2/28", "Prepare Q2 budget proposal", "Identify duplicate efforts"],
            "related_use_cases": ["UC001", "UC002", "UC003", "UC008"]
        },
    ]
    return pd.DataFrame(meetings)


# Helper function to get company name from ID
def get_company_name(company_id):
    for company in MEMBER_COMPANIES:
        if company["id"] == company_id:
            return company["name"]
    if company_id == "ASSOC":
        return "DDPA Association"
    if company_id == "SNOWFLAKE":
        return "Snowflake"
    return company_id


# Helper function to get company color
def get_company_color(company_id):
    for company in MEMBER_COMPANIES:
        if company["id"] == company_id:
            return company["color"]
    if company_id == "ASSOC":
        return "#2C3E50"
    if company_id == "SNOWFLAKE":
        return "#29B5E8"
    return "#666666"


# Financial Spend Data by Member Company
def get_monthly_spend():
    """Get monthly Snowflake spend by member company."""
    spend_data = [
        # 2024 Monthly Spend (in thousands)
        {"month": "2024-01", "CA": 185, "MA": 92, "NY": 78, "PA": 65, "TX": 58, "IL": 42, "HI": 0, "WA": 0},
        {"month": "2024-02", "CA": 192, "MA": 98, "NY": 82, "PA": 68, "TX": 62, "IL": 45, "HI": 0, "WA": 0},
        {"month": "2024-03", "CA": 201, "MA": 105, "NY": 88, "PA": 72, "TX": 68, "IL": 52, "HI": 5, "WA": 0},
        {"month": "2024-04", "CA": 198, "MA": 110, "NY": 92, "PA": 75, "TX": 72, "IL": 58, "HI": 12, "WA": 0},
        {"month": "2024-05", "CA": 215, "MA": 118, "NY": 98, "PA": 82, "TX": 78, "IL": 62, "HI": 18, "WA": 3},
        {"month": "2024-06", "CA": 225, "MA": 125, "NY": 105, "PA": 88, "TX": 85, "IL": 68, "HI": 25, "WA": 8},
        {"month": "2024-07", "CA": 232, "MA": 132, "NY": 112, "PA": 92, "TX": 88, "IL": 72, "HI": 32, "WA": 12},
        {"month": "2024-08", "CA": 245, "MA": 138, "NY": 118, "PA": 98, "TX": 92, "IL": 78, "HI": 38, "WA": 18},
        {"month": "2024-09", "CA": 252, "MA": 145, "NY": 125, "PA": 105, "TX": 98, "IL": 82, "HI": 45, "WA": 22},
        {"month": "2024-10", "CA": 268, "MA": 152, "NY": 132, "PA": 112, "TX": 105, "IL": 88, "HI": 52, "WA": 28},
        {"month": "2024-11", "CA": 275, "MA": 158, "NY": 138, "PA": 118, "TX": 112, "IL": 92, "HI": 58, "WA": 32},
        {"month": "2024-12", "CA": 285, "MA": 165, "NY": 145, "PA": 125, "TX": 118, "IL": 98, "HI": 65, "WA": 38},
    ]
    return pd.DataFrame(spend_data)


def get_investment_allocations():
    """Get investment spend allocations ($350K training budget + partner engagements)."""
    allocations = [
        {"id": "INV001", "category": "Training", "description": "Snowflake University Licenses", "amount": 75000, "status": "Completed", "beneficiary": "ALL", "date": "2024-01-15"},
        {"id": "INV002", "category": "Training", "description": "Hands-on Lab Infrastructure", "amount": 45000, "status": "Completed", "beneficiary": "ALL", "date": "2024-02-01"},
        {"id": "INV003", "category": "Partner", "description": "Huhn RSA Engagement - Data Architecture", "amount": 85000, "status": "In Progress", "beneficiary": "CA", "date": "2024-03-01"},
        {"id": "INV004", "category": "Training", "description": "ML/AI Workshop Series", "amount": 35000, "status": "Planned", "beneficiary": "ALL", "date": "2024-04-15"},
        {"id": "INV005", "category": "Partner", "description": "Integration Support - Hawaii Onboarding", "amount": 42000, "status": "In Progress", "beneficiary": "HI", "date": "2024-05-01"},
        {"id": "INV006", "category": "Project", "description": "National Data Platform - Phase 1", "amount": 125000, "status": "In Progress", "beneficiary": "NATIONAL", "date": "2024-01-01"},
        {"id": "INV007", "category": "Training", "description": "Cortex AI Certification Program", "amount": 28000, "status": "Planned", "beneficiary": "ALL", "date": "2024-06-01"},
        {"id": "INV008", "category": "Partner", "description": "Security Assessment - RSA", "amount": 55000, "status": "Completed", "beneficiary": "ALL", "date": "2024-02-15"},
    ]
    return pd.DataFrame(allocations)


def get_marketplace_drawdowns():
    """Get marketplace capacity drawdown tracking."""
    drawdowns = [
        {"id": "MP001", "company": "CA", "product": "Snowflake Cortex", "amount": 15000, "date": "2024-02-01", "billback_status": "Completed"},
        {"id": "MP002", "company": "MA", "product": "Snowpark Container Services", "amount": 8500, "date": "2024-03-15", "billback_status": "Completed"},
        {"id": "MP003", "company": "TX", "product": "Dynamic Tables", "amount": 6200, "date": "2024-04-01", "billback_status": "Pending"},
        {"id": "MP004", "company": "NY", "product": "Snowflake Cortex", "amount": 12000, "date": "2024-05-01", "billback_status": "Pending"},
        {"id": "MP005", "company": "CA", "product": "Data Clean Rooms", "amount": 22000, "date": "2024-05-15", "billback_status": "Pending"},
        {"id": "MP006", "company": "PA", "product": "Snowpark ML", "amount": 9800, "date": "2024-06-01", "billback_status": "Not Started"},
    ]
    return pd.DataFrame(drawdowns)


# Meeting Cadence Tracking
def get_scheduled_meetings():
    """Get scheduled recurring meetings."""
    from datetime import datetime, timedelta
    
    base_date = datetime(2024, 1, 1)
    meetings = []
    
    # Generate Operations Work Group meetings (Monthly, moving to Quarterly)
    for i in range(12):
        meeting_date = base_date + timedelta(days=30*i)
        meetings.append({
            "id": f"OWG-{i+1:03d}",
            "type": "Operations Work Group",
            "tier": "operations_work_group",
            "date": meeting_date.strftime("%Y-%m-%d"),
            "status": "Completed" if i < 6 else "Scheduled",
            "attendees_expected": 12,
            "notes": f"Monthly Operations Review - {meeting_date.strftime('%B %Y')}"
        })
    
    # Generate Steering Committee meetings (Monthly)
    for i in range(12):
        meeting_date = base_date + timedelta(days=30*i + 15)  # Mid-month
        meetings.append({
            "id": f"SC-{i+1:03d}",
            "type": "Steering Committee",
            "tier": "steering_committee",
            "date": meeting_date.strftime("%Y-%m-%d"),
            "status": "Completed" if i < 6 else "Scheduled",
            "attendees_expected": 18,
            "notes": f"Monthly Strategic Review - {meeting_date.strftime('%B %Y')}"
        })
    
    # Generate User Community workshops (Bi-Monthly)
    workshop_topics = [
        "Snowflake Fundamentals",
        "Data Engineering Best Practices", 
        "Cortex AI Introduction",
        "Snowpark for Python",
        "Data Clean Rooms Deep Dive",
        "Performance Optimization"
    ]
    for i in range(6):
        meeting_date = base_date + timedelta(days=60*i + 7)
        meetings.append({
            "id": f"UC-{i+1:03d}",
            "type": "User Community Workshop",
            "tier": "user_community",
            "date": meeting_date.strftime("%Y-%m-%d"),
            "status": "Completed" if i < 3 else "Scheduled",
            "attendees_expected": 35,
            "notes": f"Workshop: {workshop_topics[i]}"
        })
    
    return pd.DataFrame(meetings)


# Partner/RSA Tracking
PARTNERS = [
    {"id": "P001", "name": "Huhn Consulting", "type": "RSA", "specialty": "Data Architecture", "engagement_status": "Active", "contact": "John Huhn", "email": "jhuhn@huhnconsulting.com"},
    {"id": "P002", "name": "Snowflake PS", "type": "Professional Services", "specialty": "Implementation", "engagement_status": "On-call", "contact": "PS Team", "email": "ps@snowflake.com"},
    {"id": "P003", "name": "DataOps Partners", "type": "RSA", "specialty": "ML/AI", "engagement_status": "Evaluating", "contact": "Maria Santos", "email": "msantos@dataopspartners.com"},
]
