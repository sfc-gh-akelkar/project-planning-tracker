-- =============================================================================
-- DELTA DENTAL PROJECT PLANNING TRACKER
-- Step 3: Views
-- =============================================================================
--
-- INSTRUCTIONS:
-- 1. Update the variables below to match your 01_role_setup.sql configuration
-- 2. Run this script after 02_ddl_tables.sql and 04_seed_data.sql complete
--
-- =============================================================================

-- =============================================================================
-- CONFIGURATION VARIABLES - MUST MATCH 01_role_setup.sql
-- =============================================================================
SET PROJECT_ROLE = 'DDPA_PROJECT_TRACKER_ROLE';
SET PROJECT_DATABASE = 'DDPA_PROJECT_TRACKER_DB';
SET PROJECT_WAREHOUSE = 'DDPA_PROJECT_TRACKER_WH';

-- =============================================================================
-- Set context
-- =============================================================================
USE ROLE IDENTIFIER($PROJECT_ROLE);
USE DATABASE IDENTIFIER($PROJECT_DATABASE);
USE SCHEMA DATA;
USE WAREHOUSE IDENTIFIER($PROJECT_WAREHOUSE);

-- =============================================================================
-- 1. VIEW: USE CASES WITH COMPANY INFO (Mapping view)
-- =============================================================================
CREATE OR REPLACE VIEW V_USE_CASES_WITH_COMPANY AS
SELECT 
    uc.USE_CASE_ID,
    uc.MEMBER_COMPANY_OR_AFFILIATION,
    m.COMPANY_ID,
    c.COMPANY_NAME,
    c.ABBREV AS COMPANY_ABBREV,
    c.GROUP_AND_INDIVIDUAL_AFFILIATIONS,
    uc.TYPE,
    uc.TITLE,
    uc.DESCRIPTION,
    uc.VALUE_OR_OUTCOME,
    uc.KEY_DATA_DOMAINS,
    uc.CURRENT_STATUS,
    uc.ANTICIPATED_START_DATE,
    uc.EST_TSHIRT_SIZE,
    uc.EST_TIME,
    uc.PARTNERS,
    c.BRAND_COLOR,
    c.ONBOARDING_STATUS AS COMPANY_ONBOARDING_STATUS,
    c.IS_CONTRACTED AS COMPANY_IS_CONTRACTED,
    uc.CREATED_AT,
    uc.UPDATED_AT
FROM USE_CASES uc
LEFT JOIN USE_CASE_AFFILIATION_MAPPING m 
    ON uc.MEMBER_COMPANY_OR_AFFILIATION = m.USE_CASE_AFFILIATION
LEFT JOIN COMPANIES c 
    ON m.COMPANY_ID = c.COMPANY_ID;

-- =============================================================================
-- 2. VIEW: Company coverage by operating area
-- =============================================================================
CREATE OR REPLACE VIEW V_COMPANY_COVERAGE AS
SELECT 
    c.COMPANY_ID,
    c.COMPANY_NAME,
    c.ABBREV,
    c.GROUP_AND_INDIVIDUAL_AFFILIATIONS,
    oa.OPERATING_AREAS,
    c.ONBOARDING_STATUS,
    c.IS_CONTRACTED,
    c.BRAND_COLOR
FROM COMPANIES c
LEFT JOIN MEMBER_COMPANY_OPERATING_AREAS oa 
    ON c.COMPANY_NAME = oa.MEMBER_COMPANIES;

-- =============================================================================
-- 3. VIEW: Use case summary by company
-- =============================================================================
CREATE OR REPLACE VIEW V_USE_CASE_SUMMARY_BY_COMPANY AS
SELECT 
    v.COMPANY_ID,
    v.COMPANY_NAME,
    v.COMPANY_ABBREV,
    COUNT(*) AS TOTAL_USE_CASES,
    SUM(CASE WHEN v.TYPE = 'Use Case' THEN 1 ELSE 0 END) AS USE_CASE_COUNT,
    SUM(CASE WHEN v.TYPE = 'Migration' THEN 1 ELSE 0 END) AS MIGRATION_COUNT,
    SUM(CASE WHEN v.CURRENT_STATUS = 'In Production' THEN 1 ELSE 0 END) AS IN_PRODUCTION,
    SUM(CASE WHEN v.CURRENT_STATUS IN ('In Progress', 'Implementing', 'In Development') THEN 1 ELSE 0 END) AS IN_PROGRESS,
    SUM(CASE WHEN v.CURRENT_STATUS IN ('Idea', 'Evaluation', 'Evaluating', 'Planning') THEN 1 ELSE 0 END) AS PLANNED
FROM V_USE_CASES_WITH_COMPANY v
WHERE v.COMPANY_ID IS NOT NULL
GROUP BY v.COMPANY_ID, v.COMPANY_NAME, v.COMPANY_ABBREV;

-- =============================================================================
-- 4. VIEW: Use case summary by status
-- =============================================================================
CREATE OR REPLACE VIEW V_USE_CASE_SUMMARY_BY_STATUS AS
SELECT 
    CURRENT_STATUS,
    COUNT(*) AS USE_CASE_COUNT,
    COUNT(DISTINCT MEMBER_COMPANY_OR_AFFILIATION) AS COMPANY_COUNT
FROM USE_CASES
WHERE CURRENT_STATUS IS NOT NULL
GROUP BY CURRENT_STATUS
ORDER BY USE_CASE_COUNT DESC;

-- =============================================================================
-- 5. VIEW: Contacts with company info
-- =============================================================================
CREATE OR REPLACE VIEW V_CONTACTS_WITH_COMPANY AS
SELECT 
    ct.CONTACT_ID,
    ct.NAME,
    ct.ROLE,
    ct.COMPANY_ID,
    c.COMPANY_NAME,
    c.ABBREV AS COMPANY_ABBREV,
    ct.EMAIL,
    ct.PHONE,
    ct.IS_PRIMARY,
    ct.CREATED_AT
FROM CONTACTS ct
LEFT JOIN COMPANIES c ON ct.COMPANY_ID = c.COMPANY_ID;

-- =============================================================================
-- 6. VIEW: Monthly spend with company info
-- =============================================================================
CREATE OR REPLACE VIEW V_MONTHLY_SPEND_WITH_COMPANY AS
SELECT 
    ms.MONTH_KEY,
    ms.COMPANY_ID,
    c.COMPANY_NAME,
    c.ABBREV AS COMPANY_ABBREV,
    ms.SPEND_AMOUNT_K,
    c.IS_CONTRACTED
FROM MONTHLY_SPEND ms
LEFT JOIN COMPANIES c ON ms.COMPANY_ID = c.COMPANY_ID;

-- =============================================================================
-- Verification
-- =============================================================================
SELECT 'Views Created Successfully!' AS STATUS;
SHOW VIEWS IN SCHEMA DATA;

-- =============================================================================
-- END OF VIEWS SCRIPT
-- =============================================================================
