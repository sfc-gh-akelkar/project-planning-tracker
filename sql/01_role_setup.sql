-- =============================================================================
-- DELTA DENTAL PROJECT PLANNING TRACKER
-- Step 1: Role and Infrastructure Setup
-- =============================================================================
-- 
-- INSTRUCTIONS:
-- 1. Update the variables below with your desired names
-- 2. Run this script with a role that has privileges to create roles, 
--    databases, warehouses, and grants (e.g., ACCOUNTADMIN or custom admin role)
--
-- =============================================================================

-- =============================================================================
-- CONFIGURATION VARIABLES - UPDATE THESE AS NEEDED
-- =============================================================================
SET PROJECT_ROLE = 'DDPA_PROJECT_TRACKER_ROLE';
SET PROJECT_DATABASE = 'DDPA_PROJECT_TRACKER_DB';
SET PROJECT_WAREHOUSE = 'DDPA_PROJECT_TRACKER_WH';
SET PROJECT_STAGE = 'DDPA_APP_STAGE';
-- SET YOUR_USERNAME = 'YOUR_USERNAME';  -- Uncomment and set to grant role to yourself

-- =============================================================================
-- STEP 1: Create the project role
-- =============================================================================
CREATE ROLE IF NOT EXISTS IDENTIFIER($PROJECT_ROLE)
    COMMENT = 'Role for Delta Dental Project Planning Tracker application and data';

GRANT ROLE IDENTIFIER($PROJECT_ROLE) TO ROLE SYSADMIN;

-- Uncomment to grant role to yourself:
-- GRANT ROLE IDENTIFIER($PROJECT_ROLE) TO USER IDENTIFIER($YOUR_USERNAME);

-- =============================================================================
-- STEP 2: Create database
-- =============================================================================
CREATE DATABASE IF NOT EXISTS IDENTIFIER($PROJECT_DATABASE)
    COMMENT = 'Database for Delta Dental Project Planning Tracker';

-- =============================================================================
-- STEP 3: Create schemas (must use database context)
-- =============================================================================
USE DATABASE IDENTIFIER($PROJECT_DATABASE);

CREATE SCHEMA IF NOT EXISTS APP
    COMMENT = 'Schema for Streamlit app and related objects';

CREATE SCHEMA IF NOT EXISTS DATA
    COMMENT = 'Schema for data tables and views';

-- =============================================================================
-- STEP 4: Create warehouse
-- =============================================================================
CREATE WAREHOUSE IF NOT EXISTS IDENTIFIER($PROJECT_WAREHOUSE)
    WAREHOUSE_SIZE = 'X-SMALL'
    AUTO_SUSPEND = 60
    AUTO_RESUME = TRUE
    INITIALLY_SUSPENDED = TRUE
    COMMENT = 'Warehouse for Delta Dental Project Tracker queries';

-- =============================================================================
-- STEP 5: Grant privileges to the project role
-- =============================================================================

-- Database privileges
GRANT USAGE ON DATABASE IDENTIFIER($PROJECT_DATABASE) TO ROLE IDENTIFIER($PROJECT_ROLE);

-- Schema privileges (using current database context)
GRANT USAGE ON SCHEMA APP TO ROLE IDENTIFIER($PROJECT_ROLE);
GRANT USAGE ON SCHEMA DATA TO ROLE IDENTIFIER($PROJECT_ROLE);

GRANT CREATE TABLE ON SCHEMA DATA TO ROLE IDENTIFIER($PROJECT_ROLE);
GRANT CREATE VIEW ON SCHEMA DATA TO ROLE IDENTIFIER($PROJECT_ROLE);
GRANT CREATE STAGE ON SCHEMA APP TO ROLE IDENTIFIER($PROJECT_ROLE);
GRANT CREATE STREAMLIT ON SCHEMA APP TO ROLE IDENTIFIER($PROJECT_ROLE);

-- Future grants on tables/views in DATA schema
GRANT SELECT, INSERT, UPDATE, DELETE ON FUTURE TABLES IN SCHEMA DATA TO ROLE IDENTIFIER($PROJECT_ROLE);
GRANT SELECT ON FUTURE VIEWS IN SCHEMA DATA TO ROLE IDENTIFIER($PROJECT_ROLE);

-- Warehouse privileges
GRANT USAGE ON WAREHOUSE IDENTIFIER($PROJECT_WAREHOUSE) TO ROLE IDENTIFIER($PROJECT_ROLE);

-- =============================================================================
-- STEP 6: Create internal stage for app files (using project role)
-- =============================================================================
USE ROLE IDENTIFIER($PROJECT_ROLE);
USE SCHEMA APP;
USE WAREHOUSE IDENTIFIER($PROJECT_WAREHOUSE);

CREATE STAGE IF NOT EXISTS IDENTIFIER($PROJECT_STAGE)
    DIRECTORY = (ENABLE = TRUE)
    COMMENT = 'Stage for Streamlit app files';

-- =============================================================================
-- STEP 7: Verification
-- =============================================================================
SELECT 'Setup Complete!' AS STATUS;
SHOW GRANTS TO ROLE IDENTIFIER($PROJECT_ROLE);

-- =============================================================================
-- OPTIONAL: Compute Pool for Container Runtime
-- =============================================================================
-- NOTE: Creating compute pools requires CREATE COMPUTE POOL privilege on the
-- account. This is typically only available to ACCOUNTADMIN or roles with
-- explicit grants.
--
-- Uncomment if you need a compute pool for Streamlit Container Runtime:
--
-- SET COMPUTE_POOL_NAME = 'DDPA_STREAMLIT_POOL';
-- CREATE COMPUTE POOL IF NOT EXISTS IDENTIFIER($COMPUTE_POOL_NAME)
--     MIN_NODES = 1
--     MAX_NODES = 1
--     INSTANCE_FAMILY = CPU_X64_XS
--     AUTO_SUSPEND_SECS = 300;
-- GRANT USAGE ON COMPUTE POOL IDENTIFIER($COMPUTE_POOL_NAME) TO ROLE IDENTIFIER($PROJECT_ROLE);

-- =============================================================================
-- END OF SETUP SCRIPT
-- =============================================================================
