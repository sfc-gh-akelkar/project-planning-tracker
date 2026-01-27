# Delta Dental Project Planning Tracker

**A collaborative framework for tracking use cases and roadmaps across Delta Dental member companies.**

*Co-branded solution by DDPA and Snowflake*

---

## Overview

This Streamlit application provides a comprehensive project tracking and management solution designed for Delta Dental's collaborative initiative across member companies. It enables:

- **Use Case Management** - Track and prioritize initiatives across all member companies
- **Roadmap Visualization** - Gantt-style timeline views of all projects
- **Member Company Tracking** - Individual views for each Delta Dental member
- **Contact Management** - Subcommittee and key stakeholder information
- **Financial Tracking** - Monitor spend, investments, and marketplace drawdowns

---

## Quick Start: Deploying to Snowflake

This application is designed to run as **Streamlit in Snowflake (SiS)**. All data is pulled from Snowflake tables.

### Prerequisites

- Snowflake account
- A role with the following privileges (e.g., `ACCOUNTADMIN` or a custom admin role):
  - `CREATE ROLE` on the account
  - `CREATE DATABASE` on the account
  - `CREATE WAREHOUSE` on the account
  - `MANAGE GRANTS` on the account (to grant privileges to the new role)
  - `CREATE STREAMLIT` on the schema (granted to project role)
  - `CREATE STAGE` on the schema (granted to project role)
- For Streamlit Container Runtime (optional):
  - `CREATE COMPUTE POOL` on the account
  - `USAGE` on compute pool (granted to project role)
- Snowflake CLI (`snow`) installed (optional, for CLI deployment)

### Step 1: Configure Variables

Each SQL script has a **configuration section at the top** where you set your preferred names once:

```sql
-- =============================================================================
-- CONFIGURATION VARIABLES - UPDATE THESE AS NEEDED
-- =============================================================================
SET PROJECT_ROLE = 'DDPA_PROJECT_TRACKER_ROLE';
SET PROJECT_DATABASE = 'DDPA_PROJECT_TRACKER_DB';
SET PROJECT_WAREHOUSE = 'DDPA_PROJECT_TRACKER_WH';
SET PROJECT_STAGE = 'DDPA_APP_STAGE';
```

**To customize:** Simply change the values in the `SET` statements. The rest of the script uses these variables automatically via `IDENTIFIER($PROJECT_ROLE)` syntax.

### Step 2: Create Role and Infrastructure

Run with your privileged role:

```bash
# Using Snowflake CLI
snow sql -f sql/01_role_setup.sql

# Or execute in Snowsight/SnowSQL
```

This script creates:
- Project role (default: `DDPA_PROJECT_TRACKER_ROLE`)
- Database with `APP` and `DATA` schemas
- X-Small warehouse for queries
- Internal stage for app files
- All necessary privileges

**Grant the role to yourself** (uncomment in the script or run manually):
```sql
GRANT ROLE IDENTIFIER($PROJECT_ROLE) TO USER YOUR_USERNAME;
```

### Step 3: Create Data Tables

**Ensure the same variables are set**, then run:

```bash
snow sql -f sql/02_ddl_tables.sql
```

### Step 4: Load Seed Data

```bash
snow sql -f sql/04_seed_data.sql
```

This loads:
- 56 member company operating areas
- 45+ unique companies
- 86 use cases
- Reference data (statuses, t-shirt sizes, data domains)

### Step 5: Create Views

```bash
snow sql -f sql/03_views.sql
```

### Step 6: Deploy Streamlit App

**Option A: Using Snowflake CLI (Recommended)**

1. Update `snowflake.yml` with your compute pool:
```yaml
entities:
  ddpa_project_tracker:
    type: streamlit
    identifier:
      name: DDPA_PROJECT_TRACKER
      database: DDPA_PROJECT_TRACKER_DB
      schema: APP
    title: "Delta Dental Project Planning Tracker"
    runtime_name: SYSTEM$ST_CONTAINER_RUNTIME_PY3_11
    compute_pool: YOUR_COMPUTE_POOL  # Replace with your compute pool
    query_warehouse: DDPA_PROJECT_TRACKER_WH
    main_file: streamlit_app.py
    artifacts:
      - streamlit_app.py
      - environment.yml
      - assets/
      - SNOW-ICON.png
      - Snowflake-Logo.png
```

2. Deploy:
```bash
snow streamlit deploy --open
```

**Option B: Using SQL**

```sql
USE ROLE DDPA_PROJECT_TRACKER_ROLE;
USE DATABASE DDPA_PROJECT_TRACKER_DB;
USE SCHEMA APP;

-- Upload files to stage first
PUT file:///path/to/streamlit_app.py @DDPA_APP_STAGE AUTO_COMPRESS=FALSE OVERWRITE=TRUE;
PUT file:///path/to/environment.yml @DDPA_APP_STAGE AUTO_COMPRESS=FALSE OVERWRITE=TRUE;
-- ... upload remaining files ...

-- Create the Streamlit app
CREATE OR REPLACE STREAMLIT DDPA_PROJECT_TRACKER
    ROOT_LOCATION = '@DDPA_PROJECT_TRACKER_DB.APP.DDPA_APP_STAGE'
    MAIN_FILE = 'streamlit_app.py'
    QUERY_WAREHOUSE = DDPA_PROJECT_TRACKER_WH
    TITLE = 'Delta Dental Project Planning Tracker';
```

**Option C: Using Snowsight UI**

1. Navigate to **Projects → Streamlit** in Snowsight
2. Click **+ Streamlit App**
3. Configure with database `DDPA_PROJECT_TRACKER_DB` and schema `APP`
4. Upload all files from this repository
5. Click **Run**

---

## SQL Scripts Reference

All scripts use **session variables** for easy customization. Update the `SET` statements at the top of each script to use your own naming conventions.

| Script | Purpose | Run Order |
|--------|---------|-----------|
| `sql/01_role_setup.sql` | Creates role, database, warehouse, privileges | 1 |
| `sql/02_ddl_tables.sql` | Creates all data tables | 2 |
| `sql/04_seed_data.sql` | Loads initial data from CSVs | 3 |
| `sql/03_views.sql` | Creates views for reporting | 4 |
| `sql/05_streamlit_deploy.sql` | Deploys Streamlit app | 5 |

**Default variable values:**
```sql
SET PROJECT_ROLE = 'DDPA_PROJECT_TRACKER_ROLE';
SET PROJECT_DATABASE = 'DDPA_PROJECT_TRACKER_DB';
SET PROJECT_WAREHOUSE = 'DDPA_PROJECT_TRACKER_WH';
SET PROJECT_STAGE = 'DDPA_APP_STAGE';
```

---

## Role Hierarchy

```
ACCOUNTADMIN
    └── SYSADMIN
            └── <PROJECT_ROLE> (e.g., DDPA_PROJECT_TRACKER_ROLE)
```

**Project role privileges:**
- USAGE on project database
- USAGE on schemas `APP` and `DATA`
- CREATE TABLE, CREATE VIEW on `DATA` schema
- CREATE STREAMLIT, CREATE STAGE on `APP` schema
- SELECT, INSERT, UPDATE, DELETE on all tables
- USAGE on project warehouse

---

## Data Model

### Core Tables

| Table | Description |
|-------|-------------|
| `COMPANIES` | Unique Delta Dental member companies with metadata |
| `USE_CASES` | All use cases and migrations from member companies |
| `CONTACTS` | Key contacts and stakeholders |
| `MEETINGS` | Governance meetings and workshops |
| `MONTHLY_SPEND` | Snowflake consumption by company |
| `INVESTMENTS` | Training and partner investments |
| `MARKETPLACE_DRAWDOWNS` | Marketplace product usage |
| `PARTNERS` | RSA and partner engagements |

### Mapping Tables

| Table | Description |
|-------|-------------|
| `MEMBER_COMPANY_OPERATING_AREAS` | Member company operating area data |
| `USE_CASE_AFFILIATION_MAPPING` | Maps use case affiliations to company IDs |

### Views

| View | Description |
|------|-------------|
| `V_USE_CASES_WITH_COMPANY` | Use cases joined with company info |
| `V_COMPANY_COVERAGE` | Companies with their operating areas |
| `V_USE_CASE_SUMMARY_BY_COMPANY` | Use case counts by company |
| `V_USE_CASE_SUMMARY_BY_STATUS` | Use case counts by status |
| `V_CONTACTS_WITH_COMPANY` | Contacts with company details |
| `V_MONTHLY_SPEND_WITH_COMPANY` | Spend data with company names |

---

## Project Structure

```
project-planning-tracker/
├── streamlit_app.py              # Main Streamlit application (single file)
├── requirements.txt              # Python dependencies
├── environment.yml               # SiS container runtime dependencies
├── snowflake.yml                 # Snowflake CLI deployment config
├── README.md                     # This file
├── sql/
│   ├── 01_role_setup.sql         # Role and infrastructure setup
│   ├── 02_ddl_tables.sql         # Table DDL
│   ├── 03_views.sql              # View definitions
│   ├── 04_seed_data.sql          # Initial data load
│   └── 05_streamlit_deploy.sql   # App deployment SQL
├── assets/
│   ├── delta-dental-logo.webp
│   └── snowflake-logo.svg
├── SNOW-ICON.png
├── Snowflake-Logo.png
└── .streamlit/
    └── config.toml               # Streamlit configuration
```

---

## Features

### Dashboard
- Real-time metrics across all use cases
- Status distribution and category analysis
- Company activity breakdown
- Recent use cases display

### Governance
- **Three-Tiered Structure:**
  - Umbrella Deal Operations Work Group (DDPA + 6 contracted MCs)
  - Snowflake Steering Committee (monthly strategic oversight)
  - Snowflake User Community (workshops & training)
- Member company onboarding status tracking
- Partner/RSA engagement management

### Financial Tracking
- **$15M Commitment Monitoring:**
  - Monthly spend by member company
  - YTD consumption tracking
  - Remaining balance projections
- **$350K Training Budget:**
  - Investment allocations (Training, Partner, Project)
  - Budget utilization tracking
- **Marketplace Capacity:**
  - Drawdown tracking by product
  - Billback status management

### Use Cases
- Full CRUD operations for use cases
- Card and table views
- Advanced filtering by company, status, category
- Export to Excel

### Roadmap
- Interactive Gantt chart visualization
- Color-coding by status
- Timeline view of all projects

### Member Companies
- Individual company views with key contacts, use cases, progress metrics
- Onboarding phase tracking

### Meetings
- Operations Work Group, Steering Committee, User Community Workshops
- Upcoming meeting calendar

### Contacts
- Contact directory with company assignments
- Primary contact identification

### Settings
- Data connection info
- Refresh data from Snowflake

---

## Troubleshooting

### Common Issues

**"Insufficient privileges" error:**
```sql
-- Verify your role has the project role granted
SHOW GRANTS TO USER YOUR_USERNAME;

-- Grant if missing (use your configured role name)
USE ROLE SECURITYADMIN;
GRANT ROLE <PROJECT_ROLE> TO USER YOUR_USERNAME;
```

**"Object does not exist" error:**
```sql
-- Verify you're using the correct role and context
USE ROLE <PROJECT_ROLE>;
USE DATABASE <PROJECT_DATABASE>;
USE SCHEMA DATA;

-- Check if tables exist
SHOW TABLES;
```

**Compute pool not available:**
- Compute pools must be created by `ACCOUNTADMIN`
- Contact your Snowflake administrator to create one

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## License

This project is proprietary to the DDPA and Snowflake partnership.

---

**Built with Snowflake & Streamlit**
