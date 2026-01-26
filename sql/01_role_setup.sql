-- =============================================================================
-- DELTA DENTAL PROJECT PLANNING TRACKER
-- Step 1: Role and Privilege Setup
-- =============================================================================
-- 
-- INSTRUCTIONS:
-- 1. Update the variables below with your desired names
-- 2. Run this script as SECURITYADMIN (or a role with CREATE ROLE privilege)
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
-- STEP 1: Create the project role (requires SECURITYADMIN)
-- =============================================================================
USE ROLE SECURITYADMIN;

CREATE ROLE IF NOT EXISTS IDENTIFIER($PROJECT_ROLE)
    COMMENT = 'Role for Delta Dental Project Planning Tracker application and data';

GRANT ROLE IDENTIFIER($PROJECT_ROLE) TO ROLE SYSADMIN;

-- Uncomment to grant role to yourself:
-- GRANT ROLE IDENTIFIER($PROJECT_ROLE) TO USER IDENTIFIER($YOUR_USERNAME);

-- =============================================================================
-- STEP 2: Create database and schemas (requires SYSADMIN)
-- =============================================================================
USE ROLE SYSADMIN;

CREATE DATABASE IF NOT EXISTS IDENTIFIER($PROJECT_DATABASE)
    COMMENT = 'Database for Delta Dental Project Planning Tracker';

CREATE SCHEMA IF NOT EXISTS IDENTIFIER($PROJECT_DATABASE || '.APP')
    COMMENT = 'Schema for Streamlit app and related objects';

CREATE SCHEMA IF NOT EXISTS IDENTIFIER($PROJECT_DATABASE || '.DATA')
    COMMENT = 'Schema for data tables and views';

-- =============================================================================
-- STEP 3: Create warehouse
-- =============================================================================
CREATE WAREHOUSE IF NOT EXISTS IDENTIFIER($PROJECT_WAREHOUSE)
    WAREHOUSE_SIZE = 'X-SMALL'
    AUTO_SUSPEND = 60
    AUTO_RESUME = TRUE
    INITIALLY_SUSPENDED = TRUE
    COMMENT = 'Warehouse for Delta Dental Project Tracker queries';

-- =============================================================================
-- STEP 4: Grant privileges to the project role
-- =============================================================================
USE ROLE SECURITYADMIN;

-- Database privileges
GRANT USAGE ON DATABASE IDENTIFIER($PROJECT_DATABASE) TO ROLE IDENTIFIER($PROJECT_ROLE);

-- Schema privileges
GRANT USAGE ON SCHEMA IDENTIFIER($PROJECT_DATABASE || '.APP') TO ROLE IDENTIFIER($PROJECT_ROLE);
GRANT USAGE ON SCHEMA IDENTIFIER($PROJECT_DATABASE || '.DATA') TO ROLE IDENTIFIER($PROJECT_ROLE);

GRANT CREATE TABLE ON SCHEMA IDENTIFIER($PROJECT_DATABASE || '.DATA') TO ROLE IDENTIFIER($PROJECT_ROLE);
GRANT CREATE VIEW ON SCHEMA IDENTIFIER($PROJECT_DATABASE || '.DATA') TO ROLE IDENTIFIER($PROJECT_ROLE);
GRANT CREATE STAGE ON SCHEMA IDENTIFIER($PROJECT_DATABASE || '.APP') TO ROLE IDENTIFIER($PROJECT_ROLE);
GRANT CREATE STREAMLIT ON SCHEMA IDENTIFIER($PROJECT_DATABASE || '.APP') TO ROLE IDENTIFIER($PROJECT_ROLE);

-- Future grants on tables/views in DATA schema
GRANT SELECT, INSERT, UPDATE, DELETE ON FUTURE TABLES IN SCHEMA IDENTIFIER($PROJECT_DATABASE || '.DATA') TO ROLE IDENTIFIER($PROJECT_ROLE);
GRANT SELECT ON FUTURE VIEWS IN SCHEMA IDENTIFIER($PROJECT_DATABASE || '.DATA') TO ROLE IDENTIFIER($PROJECT_ROLE);

-- Warehouse privileges
GRANT USAGE ON WAREHOUSE IDENTIFIER($PROJECT_WAREHOUSE) TO ROLE IDENTIFIER($PROJECT_ROLE);

-- =============================================================================
-- STEP 5: Create internal stage for app files
-- =============================================================================
USE ROLE IDENTIFIER($PROJECT_ROLE);
USE DATABASE IDENTIFIER($PROJECT_DATABASE);
USE SCHEMA APP;
USE WAREHOUSE IDENTIFIER($PROJECT_WAREHOUSE);

CREATE STAGE IF NOT EXISTS IDENTIFIER($PROJECT_STAGE)
    DIRECTORY = (ENABLE = TRUE)
    COMMENT = 'Stage for Streamlit app files';

-- =============================================================================
-- STEP 6: Verification
-- =============================================================================
SELECT 'Role Setup Complete!' AS STATUS;
SHOW GRANTS TO ROLE IDENTIFIER($PROJECT_ROLE);

-- =============================================================================
-- OPTIONAL: Compute Pool (requires ACCOUNTADMIN)
-- =============================================================================
-- Uncomment and run separately if you need a compute pool for Container Runtime:
--
-- SET COMPUTE_POOL_NAME = 'DDPA_STREAMLIT_POOL';
-- USE ROLE ACCOUNTADMIN;
-- CREATE COMPUTE POOL IF NOT EXISTS IDENTIFIER($COMPUTE_POOL_NAME)
--     MIN_NODES = 1
--     MAX_NODES = 1
--     INSTANCE_FAMILY = CPU_X64_XS
--     AUTO_SUSPEND_SECS = 300;
-- GRANT USAGE ON COMPUTE POOL IDENTIFIER($COMPUTE_POOL_NAME) TO ROLE IDENTIFIER($PROJECT_ROLE);

-- =============================================================================
-- END OF ROLE SETUP SCRIPT
-- =============================================================================
