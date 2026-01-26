-- =============================================================================
-- DELTA DENTAL PROJECT PLANNING TRACKER
-- Step 5: Streamlit App Deployment
-- =============================================================================
--
-- INSTRUCTIONS:
-- 1. Update the variables below to match your 01_role_setup.sql configuration
-- 2. Ensure all app files are uploaded to the stage before running
-- 3. Update COMPUTE_POOL if using Container Runtime
--
-- =============================================================================

-- =============================================================================
-- CONFIGURATION VARIABLES - MUST MATCH 01_role_setup.sql
-- =============================================================================
SET PROJECT_ROLE = 'DDPA_PROJECT_TRACKER_ROLE';
SET PROJECT_DATABASE = 'DDPA_PROJECT_TRACKER_DB';
SET PROJECT_WAREHOUSE = 'DDPA_PROJECT_TRACKER_WH';
SET PROJECT_STAGE = 'DDPA_APP_STAGE';
SET STREAMLIT_APP_NAME = 'DDPA_PROJECT_TRACKER';
-- SET COMPUTE_POOL = 'DDPA_STREAMLIT_POOL';  -- Uncomment for Container Runtime

-- =============================================================================
-- Set context
-- =============================================================================
USE ROLE IDENTIFIER($PROJECT_ROLE);
USE DATABASE IDENTIFIER($PROJECT_DATABASE);
USE SCHEMA APP;
USE WAREHOUSE IDENTIFIER($PROJECT_WAREHOUSE);

-- =============================================================================
-- Step 1: Verify stage exists and has files
-- =============================================================================
LIST @IDENTIFIER($PROJECT_STAGE);

-- =============================================================================
-- Step 2: Create the Streamlit app (Native Runtime - no compute pool needed)
-- =============================================================================
CREATE OR REPLACE STREAMLIT IDENTIFIER($STREAMLIT_APP_NAME)
    ROOT_LOCATION = '@' || $PROJECT_DATABASE || '.APP.' || $PROJECT_STAGE
    MAIN_FILE = 'streamlit_app.py'
    QUERY_WAREHOUSE = IDENTIFIER($PROJECT_WAREHOUSE)
    TITLE = 'Delta Dental Project Planning Tracker'
    COMMENT = 'Collaborative project tracking for Delta Dental member companies';

-- =============================================================================
-- Step 3: Get the app URL
-- =============================================================================
SHOW STREAMLITS LIKE 'DDPA_PROJECT_TRACKER';

SELECT 'Streamlit App Deployed Successfully!' AS STATUS;

-- =============================================================================
-- OPTIONAL: Container Runtime (requires compute pool)
-- =============================================================================
-- If you need Container Runtime features, uncomment and update COMPUTE_POOL above,
-- then run this instead of Step 2:
--
-- CREATE OR REPLACE STREAMLIT IDENTIFIER($STREAMLIT_APP_NAME)
--     ROOT_LOCATION = '@' || $PROJECT_DATABASE || '.APP.' || $PROJECT_STAGE
--     MAIN_FILE = 'streamlit_app.py'
--     QUERY_WAREHOUSE = IDENTIFIER($PROJECT_WAREHOUSE)
--     RUNTIME_NAME = 'SYSTEM$ST_CONTAINER_RUNTIME_PY3_11'
--     COMPUTE_POOL = IDENTIFIER($COMPUTE_POOL)
--     TITLE = 'Delta Dental Project Planning Tracker'
--     COMMENT = 'Collaborative project tracking for Delta Dental member companies';

-- =============================================================================
-- END OF STREAMLIT DEPLOYMENT SCRIPT
-- =============================================================================
