-- =============================================================================
-- DELTA DENTAL PROJECT PLANNING TRACKER
-- Step 2: Data Tables DDL
-- =============================================================================
--
-- INSTRUCTIONS:
-- 1. Update the variables below to match your 01_role_setup.sql configuration
-- 2. Run this script after 01_role_setup.sql completes successfully
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
-- 1. MEMBER COMPANY OPERATING AREAS (Raw CSV data from mc_list.csv)
-- =============================================================================
CREATE OR REPLACE TABLE MEMBER_COMPANY_OPERATING_AREAS (
    GROUP_AND_INDIVIDUAL_AFFILIATIONS VARCHAR(200),
    OPERATING_AREAS VARCHAR(50),
    MEMBER_COMPANIES VARCHAR(100),
    CREATED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    PRIMARY KEY (OPERATING_AREAS, MEMBER_COMPANIES)
);

-- =============================================================================
-- 2. COMPANIES (Unique companies with IDs for foreign key references)
-- =============================================================================
CREATE OR REPLACE TABLE COMPANIES (
    COMPANY_ID VARCHAR(20) PRIMARY KEY,
    COMPANY_NAME VARCHAR(100) NOT NULL,
    GROUP_AND_INDIVIDUAL_AFFILIATIONS VARCHAR(200),
    ABBREV VARCHAR(20),
    BRAND_COLOR VARCHAR(7) DEFAULT '#1E88E5',
    ONBOARDING_STATUS VARCHAR(20) DEFAULT 'Evaluating',
    ONBOARDING_PHASE VARCHAR(50),
    ONBOARDED_DATE DATE,
    IS_CONTRACTED BOOLEAN DEFAULT FALSE,
    CREATED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    UPDATED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- =============================================================================
-- 3. USE CASE AFFILIATION MAPPING (Maps use case affiliations to companies)
-- =============================================================================
CREATE OR REPLACE TABLE USE_CASE_AFFILIATION_MAPPING (
    USE_CASE_AFFILIATION VARCHAR(100) PRIMARY KEY,
    COMPANY_ID VARCHAR(20),
    DESCRIPTION VARCHAR(200),
    CREATED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- =============================================================================
-- 4. USE CASES (Raw CSV data from use_case_list.csv)
-- =============================================================================
CREATE OR REPLACE TABLE USE_CASES (
    USE_CASE_ID NUMBER AUTOINCREMENT PRIMARY KEY,
    MEMBER_COMPANY_OR_AFFILIATION VARCHAR(100),
    TYPE VARCHAR(50),
    TITLE VARCHAR(200),
    DESCRIPTION TEXT,
    VALUE_OR_OUTCOME VARCHAR(500),
    KEY_DATA_DOMAINS VARCHAR(100),
    CURRENT_STATUS VARCHAR(50),
    ANTICIPATED_START_DATE VARCHAR(50),
    EST_TSHIRT_SIZE VARCHAR(10),
    EST_TIME VARCHAR(50),
    PARTNERS VARCHAR(200),
    CREATED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    UPDATED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- =============================================================================
-- 5. CONTACTS
-- =============================================================================
CREATE OR REPLACE TABLE CONTACTS (
    CONTACT_ID VARCHAR(20) PRIMARY KEY,
    NAME VARCHAR(100) NOT NULL,
    ROLE VARCHAR(100),
    COMPANY_ID VARCHAR(20) REFERENCES COMPANIES(COMPANY_ID),
    EMAIL VARCHAR(100),
    PHONE VARCHAR(20),
    IS_PRIMARY BOOLEAN DEFAULT FALSE,
    CREATED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    UPDATED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- =============================================================================
-- 6. CONTACT SUBCOMMITTEES (Many-to-many)
-- =============================================================================
CREATE OR REPLACE TABLE CONTACT_SUBCOMMITTEES (
    CONTACT_ID VARCHAR(20) REFERENCES CONTACTS(CONTACT_ID),
    SUBCOMMITTEE VARCHAR(50),
    CREATED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    PRIMARY KEY (CONTACT_ID, SUBCOMMITTEE)
);

-- =============================================================================
-- 7. MEETINGS
-- =============================================================================
CREATE OR REPLACE TABLE MEETINGS (
    MEETING_ID VARCHAR(20) PRIMARY KEY,
    MEETING_TYPE VARCHAR(100),
    GOVERNANCE_TIER VARCHAR(30),
    MEETING_DATE DATE NOT NULL,
    STATUS VARCHAR(20),
    ATTENDEES_EXPECTED NUMBER,
    NOTES TEXT,
    CREATED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    UPDATED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- =============================================================================
-- 8. MONTHLY SPEND
-- =============================================================================
CREATE OR REPLACE TABLE MONTHLY_SPEND (
    MONTH_KEY VARCHAR(7) NOT NULL,
    COMPANY_ID VARCHAR(20) REFERENCES COMPANIES(COMPANY_ID),
    SPEND_AMOUNT_K NUMBER(10,2),
    CREATED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    PRIMARY KEY (MONTH_KEY, COMPANY_ID)
);

-- =============================================================================
-- 9. INVESTMENTS
-- =============================================================================
CREATE OR REPLACE TABLE INVESTMENTS (
    INVESTMENT_ID VARCHAR(20) PRIMARY KEY,
    CATEGORY VARCHAR(30),
    DESCRIPTION VARCHAR(200),
    AMOUNT NUMBER(12,2),
    STATUS VARCHAR(20),
    BENEFICIARY VARCHAR(50),
    INVESTMENT_DATE DATE,
    CREATED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    UPDATED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- =============================================================================
-- 10. MARKETPLACE DRAWDOWNS
-- =============================================================================
CREATE OR REPLACE TABLE MARKETPLACE_DRAWDOWNS (
    DRAWDOWN_ID VARCHAR(20) PRIMARY KEY,
    COMPANY_ID VARCHAR(20) REFERENCES COMPANIES(COMPANY_ID),
    PRODUCT VARCHAR(100),
    AMOUNT NUMBER(12,2),
    DRAWDOWN_DATE DATE,
    BILLBACK_STATUS VARCHAR(20),
    CREATED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    UPDATED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- =============================================================================
-- 11. PARTNERS
-- =============================================================================
CREATE OR REPLACE TABLE PARTNERS (
    PARTNER_ID VARCHAR(20) PRIMARY KEY,
    NAME VARCHAR(100) NOT NULL,
    PARTNER_TYPE VARCHAR(30),
    SPECIALTY VARCHAR(100),
    ENGAGEMENT_STATUS VARCHAR(20),
    CONTACT_NAME VARCHAR(100),
    EMAIL VARCHAR(100),
    CREATED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    UPDATED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- =============================================================================
-- 12. REFERENCE TABLES
-- =============================================================================
CREATE OR REPLACE TABLE REF_STATUSES (
    STATUS VARCHAR(50) PRIMARY KEY,
    SORT_ORDER NUMBER,
    STATUS_TYPE VARCHAR(20)
);

CREATE OR REPLACE TABLE REF_TSHIRT_SIZES (
    SIZE_CODE VARCHAR(10) PRIMARY KEY,
    SIZE_NAME VARCHAR(20),
    SORT_ORDER NUMBER,
    TYPICAL_DURATION VARCHAR(50)
);

CREATE OR REPLACE TABLE REF_DATA_DOMAINS (
    DOMAIN VARCHAR(50) PRIMARY KEY,
    DESCRIPTION VARCHAR(200)
);

CREATE OR REPLACE TABLE REF_GOVERNANCE_TIERS (
    TIER_KEY VARCHAR(30) PRIMARY KEY,
    TIER_NAME VARCHAR(100),
    DESCRIPTION TEXT,
    CADENCE VARCHAR(50)
);

-- =============================================================================
-- Verification
-- =============================================================================
SELECT 'Tables Created Successfully!' AS STATUS;
SHOW TABLES IN SCHEMA DATA;

-- =============================================================================
-- END OF DDL SCRIPT
-- =============================================================================
