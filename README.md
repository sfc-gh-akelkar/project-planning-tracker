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

- Snowflake account with Snowsight access
- A role with the following privileges (e.g., `ACCOUNTADMIN` or a custom admin role):
  - `CREATE ROLE` on the account
  - `CREATE DATABASE` on the account
  - `CREATE WAREHOUSE` on the account
  - `MANAGE GRANTS` on the account
  - `CREATE STREAMLIT` on the schema
  - `CREATE STAGE` on the schema

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

**To customize:** Simply change the values in the `SET` statements. The rest of the script uses these variables automatically.

### Step 2: Run SQL Scripts in Snowsight

Open each SQL file in Snowsight and execute in order:

1. **`sql/01_role_setup.sql`** - Creates role, database, warehouse, and privileges
2. **`sql/02_ddl_tables.sql`** - Creates all data tables
3. **`sql/04_seed_data.sql`** - Loads initial seed data
4. **`sql/03_views.sql`** - Creates views for reporting

**Grant the role to yourself** (uncomment in the script or run manually):
```sql
GRANT ROLE IDENTIFIER($PROJECT_ROLE) TO USER YOUR_USERNAME;
```

### Step 3: Deploy Streamlit App

**Option A: Using Snowsight UI (Recommended)**

1. Navigate to **Projects → Streamlit** in Snowsight
2. Click **+ Streamlit App**
3. Select database `DDPA_PROJECT_TRACKER_DB` and schema `APP`
4. Select warehouse `DDPA_PROJECT_TRACKER_WH`
5. Upload `streamlit_app.py` and `environment.yml`
6. Upload `assets/` folder contents
7. Upload `SNOW-ICON.png` and `Snowflake-Logo.png`
8. Click **Run**

**Option B: Using SQL**

First, upload files to the stage, then run `sql/05_streamlit_deploy.sql`:

```sql
USE ROLE DDPA_PROJECT_TRACKER_ROLE;
USE DATABASE DDPA_PROJECT_TRACKER_DB;
USE SCHEMA APP;

-- Upload files to stage
PUT file:///path/to/streamlit_app.py @DDPA_APP_STAGE AUTO_COMPRESS=FALSE OVERWRITE=TRUE;
PUT file:///path/to/environment.yml @DDPA_APP_STAGE AUTO_COMPRESS=FALSE OVERWRITE=TRUE;
PUT file:///path/to/SNOW-ICON.png @DDPA_APP_STAGE AUTO_COMPRESS=FALSE OVERWRITE=TRUE;
PUT file:///path/to/Snowflake-Logo.png @DDPA_APP_STAGE AUTO_COMPRESS=FALSE OVERWRITE=TRUE;
PUT file:///path/to/assets/delta-dental-logo.webp @DDPA_APP_STAGE/assets/ AUTO_COMPRESS=FALSE OVERWRITE=TRUE;

-- Create the Streamlit app
CREATE OR REPLACE STREAMLIT DDPA_PROJECT_TRACKER
    ROOT_LOCATION = '@DDPA_PROJECT_TRACKER_DB.APP.DDPA_APP_STAGE'
    MAIN_FILE = 'streamlit_app.py'
    QUERY_WAREHOUSE = DDPA_PROJECT_TRACKER_WH
    TITLE = 'Delta Dental Project Planning Tracker';
```

---

## SQL Scripts Reference

| Script | Purpose | Run Order |
|--------|---------|-----------|
| `sql/01_role_setup.sql` | Creates role, database, warehouse, privileges | 1 |
| `sql/02_ddl_tables.sql` | Creates all data tables | 2 |
| `sql/04_seed_data.sql` | Loads initial data | 3 |
| `sql/03_views.sql` | Creates views for reporting | 4 |
| `sql/05_streamlit_deploy.sql` | Deploys Streamlit app | 5 |

---

## Role Hierarchy

```
ACCOUNTADMIN
    └── SYSADMIN
            └── DDPA_PROJECT_TRACKER_ROLE
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
| `COMPANIES` | Delta Dental member companies with metadata |
| `USE_CASES` | Use cases and migrations from member companies |
| `CONTACTS` | Key contacts and stakeholders |
| `MEETINGS` | Governance meetings and workshops |
| `MONTHLY_SPEND` | Snowflake consumption by company |
| `INVESTMENTS` | Training and partner investments |
| `MARKETPLACE_DRAWDOWNS` | Marketplace product usage |
| `PARTNERS` | RSA and partner engagements |

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
├── streamlit_app.py              # Main Streamlit application
├── environment.yml               # SiS dependencies
├── README.md                     # This file
├── sql/
│   ├── 01_role_setup.sql
│   ├── 02_ddl_tables.sql
│   ├── 03_views.sql
│   ├── 04_seed_data.sql
│   └── 05_streamlit_deploy.sql
├── assets/
│   └── delta-dental-logo.webp
├── SNOW-ICON.png
└── Snowflake-Logo.png
```

---

## Features

### Dashboard
- Real-time metrics across all use cases
- Status distribution and category analysis
- Company activity breakdown

### Governance
- Three-tiered governance structure
- Member company onboarding tracking

### Financial Tracking
- Monthly spend monitoring
- Investment allocations
- Marketplace drawdown tracking

### Use Cases
- CRUD operations for use cases
- Card and table views
- Filtering and Excel export

### Roadmap
- Gantt chart visualization
- Timeline view of projects

### Member Companies
- Individual company views
- Contacts and progress metrics

### Meetings & Contacts
- Meeting calendar
- Contact directory

---

## Troubleshooting

**"Insufficient privileges" error:**
```sql
SHOW GRANTS TO USER YOUR_USERNAME;
USE ROLE SECURITYADMIN;
GRANT ROLE DDPA_PROJECT_TRACKER_ROLE TO USER YOUR_USERNAME;
```

**"Object does not exist" error:**
```sql
USE ROLE DDPA_PROJECT_TRACKER_ROLE;
USE DATABASE DDPA_PROJECT_TRACKER_DB;
SHOW TABLES IN SCHEMA DATA;
```

---

## License

This project is proprietary to the DDPA and Snowflake partnership.

---

**Built with Snowflake & Streamlit**
