-- =============================================================================
-- DELTA DENTAL PROJECT PLANNING TRACKER
-- Complete Snowflake DDL Script
-- =============================================================================

-- -----------------------------------------------------------------------------
-- 1. MEMBER COMPANY OPERATING AREAS (Raw CSV data from mc_list.csv)
-- -----------------------------------------------------------------------------
CREATE OR REPLACE TABLE MEMBER_COMPANY_OPERATING_AREAS (
    GROUP_AND_INDIVIDUAL_AFFILIATIONS VARCHAR(200),
    OPERATING_AREAS VARCHAR(50),
    MEMBER_COMPANIES VARCHAR(100),
    PRIMARY KEY (OPERATING_AREAS, MEMBER_COMPANIES)
);

INSERT INTO MEMBER_COMPANY_OPERATING_AREAS (GROUP_AND_INDIVIDUAL_AFFILIATIONS, OPERATING_AREAS, MEMBER_COMPANIES) VALUES
('California, Pennsylvania (Midatlantic), Delta Dental Insurance Company (DDIC), and Affiliates', 'California', 'Delta Dental of California'),
('California, Pennsylvania (Midatlantic), Delta Dental Insurance Company (DDIC), and Affiliates', 'Pennsylvania', 'Delta Dental of Pennsylvania'),
('California, Pennsylvania (Midatlantic), Delta Dental Insurance Company (DDIC), and Affiliates', 'Maryland', 'Delta Dental of Pennsylvania'),
('California, Pennsylvania (Midatlantic), Delta Dental Insurance Company (DDIC), and Affiliates', 'Delaware', 'Delta Dental of Delaware'),
('California, Pennsylvania (Midatlantic), Delta Dental Insurance Company (DDIC), and Affiliates', 'Washington, D.C.', 'Delta Dental of the District of Columbia'),
('California, Pennsylvania (Midatlantic), Delta Dental Insurance Company (DDIC), and Affiliates', 'New York', 'Delta Dental of New York'),
('California, Pennsylvania (Midatlantic), Delta Dental Insurance Company (DDIC), and Affiliates', 'West Virginia', 'Delta Dental of West Virginia'),
('California, Pennsylvania (Midatlantic), Delta Dental Insurance Company (DDIC), and Affiliates', 'Alabama', 'Delta Dental Insurance Company (DDIC)'),
('California, Pennsylvania (Midatlantic), Delta Dental Insurance Company (DDIC), and Affiliates', 'Florida', 'Delta Dental Insurance Company (DDIC)'),
('California, Pennsylvania (Midatlantic), Delta Dental Insurance Company (DDIC), and Affiliates', 'Georgia', 'Delta Dental Insurance Company (DDIC)'),
('California, Pennsylvania (Midatlantic), Delta Dental Insurance Company (DDIC), and Affiliates', 'Louisiana', 'Delta Dental Insurance Company (DDIC)'),
('California, Pennsylvania (Midatlantic), Delta Dental Insurance Company (DDIC), and Affiliates', 'Mississippi', 'Delta Dental Insurance Company (DDIC)'),
('California, Pennsylvania (Midatlantic), Delta Dental Insurance Company (DDIC), and Affiliates', 'Montana', 'Delta Dental Insurance Company (DDIC)'),
('California, Pennsylvania (Midatlantic), Delta Dental Insurance Company (DDIC), and Affiliates', 'Nevada', 'Delta Dental Insurance Company (DDIC)'),
('California, Pennsylvania (Midatlantic), Delta Dental Insurance Company (DDIC), and Affiliates', 'Texas', 'Delta Dental Insurance Company (DDIC)'),
('California, Pennsylvania (Midatlantic), Delta Dental Insurance Company (DDIC), and Affiliates', 'Utah', 'Delta Dental Insurance Company (DDIC)'),
('California, Pennsylvania (Midatlantic), Delta Dental Insurance Company (DDIC), and Affiliates', 'Puerto Rico', 'Delta Dental of Puerto Rico'),
('Michigan, Indiana, Ohio, Tennessee, New Mexico, North Carolina, Kentucky, Arkansas', 'Kentucky', 'Delta Dental of Kentucky, Inc.'),
('Michigan, Indiana, Ohio, Tennessee, New Mexico, North Carolina, Kentucky, Arkansas', 'Michigan', 'Delta Dental Plan of Michigan, Inc.'),
('Michigan, Indiana, Ohio, Tennessee, New Mexico, North Carolina, Kentucky, Arkansas', 'Indiana', 'Delta Dental Plan of Indiana, Inc.'),
('Michigan, Indiana, Ohio, Tennessee, New Mexico, North Carolina, Kentucky, Arkansas', 'Ohio', 'Delta Dental Plan of Ohio, Inc.'),
('Michigan, Indiana, Ohio, Tennessee, New Mexico, North Carolina, Kentucky, Arkansas', 'Tennessee', 'Delta Dental of Tennessee'),
('Michigan, Indiana, Ohio, Tennessee, New Mexico, North Carolina, Kentucky, Arkansas', 'New Mexico', 'Delta Dental Plan of New Mexico, Inc.'),
('Michigan, Indiana, Ohio, Tennessee, New Mexico, North Carolina, Kentucky, Arkansas', 'North Carolina', 'Delta Dental of North Carolina'),
('Michigan, Indiana, Ohio, Tennessee, New Mexico, North Carolina, Kentucky, Arkansas', 'Arkansas', 'Delta Dental Plan of Arkansas, Inc.'),
('Minnesota and Affiliates', 'Nebraska', 'Delta Dental of Nebraska'),
('Minnesota and Affiliates', 'Minnesota', 'Delta Dental of Minnesota'),
('Minnesota and Affiliates', 'North Dakota', 'Delta Dental of Minnesota'),
('Arizona', 'Arizona', 'Delta Dental of Arizona, Inc.'),
('Missouri and Affiliates', 'Missouri', 'Delta Dental of Missouri'),
('Missouri and Affiliates', 'South Carolina', 'Delta Dental of Missouri'),
('Northeast Delta Dental (NEDD)', 'Maine', 'Delta Dental Plan of Maine'),
('Northeast Delta Dental (NEDD)', 'New Hampshire', 'Delta Dental Plan of New Hampshire'),
('Northeast Delta Dental (NEDD)', 'Vermont', 'Delta Dental Plan of Vermont'),
('New Jersey and Affiliates', 'New Jersey', 'Delta Dental of New Jersey'),
('New Jersey and Affiliates', 'Connecticut', 'Delta Dental of New Jersey'),
('Oregon and Affiliates', 'Oregon', 'Delta Dental of Oregon'),
('Oregon and Affiliates', 'Alaska', 'Delta Dental of Oregon'),
('Wisconsin', 'Wisconsin', 'Delta Dental of Wisconsin'),
('Illinois', 'Illinois', 'Delta Dental of Illinois'),
('Colorado', 'Colorado', 'Delta Dental of Colorado'),
('Virginia', 'Virginia', 'Delta Dental of Virginia'),
('Idaho', 'Idaho', 'Delta Dental of Idaho'),
('Wyoming', 'Wyoming', 'Delta Dental of Wyoming'),
('Hawaii', 'Hawaii', 'Hawaii Dental Service'),
('South Dakota', 'South Dakota', 'Delta Dental of South Dakota'),
('Iowa', 'Iowa', 'Delta Dental of Iowa'),
('Kansas', 'Kansas', 'Delta Dental of Kansas, Inc.'),
('Massachusetts', 'Massachusetts', 'DSM dba Delta Dental of Massachusetts, Inc.'),
('Oklahoma', 'Oklahoma', 'Delta Dental of Oklahoma'),
('Rhode Island', 'Rhode Island', 'Delta Dental of Rhode Island'),
('Washington', 'Washington', 'Delta Dental of Washington'),
('NorthWinds', 'N/A', 'N/A'),
('TriForza', 'N/A', 'N/A'),
('Advanced Health Services (AHS)', 'N/A', 'N/A'),
('SkyGen', 'N/A', 'N/A');

-- -----------------------------------------------------------------------------
-- 2. COMPANIES (Unique companies with IDs for foreign key references)
-- -----------------------------------------------------------------------------
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

INSERT INTO COMPANIES (COMPANY_ID, COMPANY_NAME, GROUP_AND_INDIVIDUAL_AFFILIATIONS, ABBREV, BRAND_COLOR, ONBOARDING_STATUS, IS_CONTRACTED) VALUES
-- DDCA Group / California, Pennsylvania (Midatlantic), DDIC, and Affiliates
('DDCA', 'Delta Dental of California', 'California, Pennsylvania (Midatlantic), Delta Dental Insurance Company (DDIC), and Affiliates', 'DDCA', '#1E88E5', 'Active', TRUE),
('DDPA', 'Delta Dental of Pennsylvania', 'California, Pennsylvania (Midatlantic), Delta Dental Insurance Company (DDIC), and Affiliates', 'DDPA', '#43A047', 'Active', TRUE),
('DDDE', 'Delta Dental of Delaware', 'California, Pennsylvania (Midatlantic), Delta Dental Insurance Company (DDIC), and Affiliates', 'DDDE', '#FB8C00', 'Evaluating', FALSE),
('DDDC', 'Delta Dental of the District of Columbia', 'California, Pennsylvania (Midatlantic), Delta Dental Insurance Company (DDIC), and Affiliates', 'DDDC', '#8E24AA', 'Evaluating', FALSE),
('DDNY', 'Delta Dental of New York', 'California, Pennsylvania (Midatlantic), Delta Dental Insurance Company (DDIC), and Affiliates', 'DDNY', '#E53935', 'Active', TRUE),
('DDWV', 'Delta Dental of West Virginia', 'California, Pennsylvania (Midatlantic), Delta Dental Insurance Company (DDIC), and Affiliates', 'DDWV', '#00ACC1', 'Evaluating', FALSE),
('DDIC', 'Delta Dental Insurance Company (DDIC)', 'California, Pennsylvania (Midatlantic), Delta Dental Insurance Company (DDIC), and Affiliates', 'DDIC', '#5E35B1', 'Active', TRUE),
('DDPR', 'Delta Dental of Puerto Rico', 'California, Pennsylvania (Midatlantic), Delta Dental Insurance Company (DDIC), and Affiliates', 'DDPR', '#F4511E', 'Evaluating', FALSE),

-- Michigan, Indiana, Ohio, Tennessee, New Mexico, North Carolina, Kentucky, Arkansas
('DDKY', 'Delta Dental of Kentucky, Inc.', 'Michigan, Indiana, Ohio, Tennessee, New Mexico, North Carolina, Kentucky, Arkansas', 'DDKY', '#7CB342', 'Evaluating', FALSE),
('DDMI', 'Delta Dental Plan of Michigan, Inc.', 'Michigan, Indiana, Ohio, Tennessee, New Mexico, North Carolina, Kentucky, Arkansas', 'DDMI', '#039BE5', 'Active', FALSE),
('DDIN', 'Delta Dental Plan of Indiana, Inc.', 'Michigan, Indiana, Ohio, Tennessee, New Mexico, North Carolina, Kentucky, Arkansas', 'DDIN', '#8E24AA', 'Evaluating', FALSE),
('DDOH', 'Delta Dental Plan of Ohio, Inc.', 'Michigan, Indiana, Ohio, Tennessee, New Mexico, North Carolina, Kentucky, Arkansas', 'DDOH', '#D81B60', 'Evaluating', FALSE),
('DDTN', 'Delta Dental of Tennessee', 'Michigan, Indiana, Ohio, Tennessee, New Mexico, North Carolina, Kentucky, Arkansas', 'DDTN', '#FDD835', 'Evaluating', FALSE),
('DDNM', 'Delta Dental Plan of New Mexico, Inc.', 'Michigan, Indiana, Ohio, Tennessee, New Mexico, North Carolina, Kentucky, Arkansas', 'DDNM', '#00897B', 'Evaluating', FALSE),
('DDNC', 'Delta Dental of North Carolina', 'Michigan, Indiana, Ohio, Tennessee, New Mexico, North Carolina, Kentucky, Arkansas', 'DDNC', '#3949AB', 'Evaluating', FALSE),
('DDAR', 'Delta Dental Plan of Arkansas, Inc.', 'Michigan, Indiana, Ohio, Tennessee, New Mexico, North Carolina, Kentucky, Arkansas', 'DDAR', '#C0CA33', 'Evaluating', FALSE),

-- Minnesota and Affiliates
('DDNE', 'Delta Dental of Nebraska', 'Minnesota and Affiliates', 'DDNE', '#FF7043', 'Evaluating', FALSE),
('DDMN', 'Delta Dental of Minnesota', 'Minnesota and Affiliates', 'DDMN', '#5C6BC0', 'Evaluating', FALSE),

-- Standalone States
('DDAZ', 'Delta Dental of Arizona, Inc.', 'Arizona', 'DDAZ', '#EC407A', 'Evaluating', FALSE),
('DDMO', 'Delta Dental of Missouri', 'Missouri and Affiliates', 'DDMO', '#AB47BC', 'Active', FALSE),
('DDWI', 'Delta Dental of Wisconsin', 'Wisconsin', 'DDWI', '#26A69A', 'Active', FALSE),
('DDIL', 'Delta Dental of Illinois', 'Illinois', 'DDIL', '#42A5F5', 'Active', TRUE),
('DDCO', 'Delta Dental of Colorado', 'Colorado', 'DDCO', '#66BB6A', 'Evaluating', FALSE),
('DDVA', 'Delta Dental of Virginia', 'Virginia', 'DDVA', '#EF5350', 'Evaluating', FALSE),
('DDID', 'Delta Dental of Idaho', 'Idaho', 'DDID', '#7E57C2', 'Planning', FALSE),
('DDWY', 'Delta Dental of Wyoming', 'Wyoming', 'DDWY', '#FFCA28', 'Evaluating', FALSE),
('DDHI', 'Hawaii Dental Service', 'Hawaii', 'DDHI', '#26C6DA', 'Evaluating', FALSE),
('DDSD', 'Delta Dental of South Dakota', 'South Dakota', 'DDSD', '#9CCC65', 'Evaluating', FALSE),
('DDIA', 'Delta Dental of Iowa', 'Iowa', 'DDIA', '#FF7043', 'Evaluation', FALSE),
('DDKS', 'Delta Dental of Kansas, Inc.', 'Kansas', 'DDKS', '#5C6BC0', 'Evaluating', FALSE),
('DDMA', 'DSM dba Delta Dental of Massachusetts, Inc.', 'Massachusetts', 'DDMA', '#29B6F6', 'Active', TRUE),
('DDOK', 'Delta Dental of Oklahoma', 'Oklahoma', 'DDOK', '#FFEE58', 'Evaluating', FALSE),
('DDRI', 'Delta Dental of Rhode Island', 'Rhode Island', 'DDRI', '#78909C', 'Evaluating', FALSE),
('DDWA', 'Delta Dental of Washington', 'Washington', 'DDWA', '#4DB6AC', 'Active', FALSE),

-- Northeast Delta Dental (NEDD)
('DDME', 'Delta Dental Plan of Maine', 'Northeast Delta Dental (NEDD)', 'DDME', '#FF8A65', 'Evaluating', FALSE),
('DDNH', 'Delta Dental Plan of New Hampshire', 'Northeast Delta Dental (NEDD)', 'DDNH', '#81C784', 'Evaluating', FALSE),
('DDVT', 'Delta Dental Plan of Vermont', 'Northeast Delta Dental (NEDD)', 'DDVT', '#4DD0E1', 'Evaluating', FALSE),
('NEDD', 'Northeast Delta Dental', 'Northeast Delta Dental (NEDD)', 'NEDD', '#7986CB', 'Evaluation', FALSE),

-- New Jersey and Affiliates
('DDNJ', 'Delta Dental of New Jersey', 'New Jersey and Affiliates', 'DDNJ', '#BA68C8', 'Idea', FALSE),

-- Oregon and Affiliates
('DDOR', 'Delta Dental of Oregon', 'Oregon and Affiliates', 'DDOR', '#4FC3F7', 'Evaluating', FALSE),

-- Other Entities (not traditional member companies)
('NORTHWINDS', 'NorthWinds', 'NorthWinds', 'NW', '#607D8B', 'In Development', FALSE),
('TRIFORZA', 'TriForza', 'TriForza', 'TFZ', '#90A4AE', 'Active', FALSE),
('AHS', 'Advanced Health Services', 'Advanced Health Services (AHS)', 'AHS', '#B0BEC5', 'Evaluating', FALSE),
('SKYGEN', 'SkyGen', 'SkyGen', 'SKY', '#78909C', 'Evaluating', FALSE),

-- Internal/National entities
('DDPA_INTERNAL', 'DDPA Internal', 'DDPA Internal Operations', 'DDPA-INT', '#43A047', 'Active', TRUE),
('DDPA_NATIONAL', 'DDPA National Reporting', 'DDPA National', 'DDPA-NAT', '#2E7D32', 'Active', TRUE),
('DDPA_TOOLS', 'DDPA National Tools', 'DDPA National', 'DDPA-TOOLS', '#388E3C', 'Active', TRUE);

-- -----------------------------------------------------------------------------
-- 3. USE CASE AFFILIATION MAPPING (Maps use case affiliations to companies)
-- -----------------------------------------------------------------------------
CREATE OR REPLACE TABLE USE_CASE_AFFILIATION_MAPPING (
    USE_CASE_AFFILIATION VARCHAR(100) PRIMARY KEY,
    COMPANY_ID VARCHAR(20),
    DESCRIPTION VARCHAR(200)
);

INSERT INTO USE_CASE_AFFILIATION_MAPPING (USE_CASE_AFFILIATION, COMPANY_ID, DESCRIPTION) VALUES
('DDCA Group', 'DDCA', 'Delta Dental of California and affiliates'),
('DDCA', 'DDCA', 'Delta Dental of California'),
('DDIA', 'DDIA', 'Delta Dental of Iowa'),
('DDID', 'DDID', 'Delta Dental of Idaho'),
('DDMI - Group', 'DDMI', 'Delta Dental of Michigan Group'),
('DDMI Group', 'DDMI', 'Delta Dental of Michigan Group'),
('DDMI', 'DDMI', 'Delta Dental of Michigan'),
('DDMO', 'DDMO', 'Delta Dental of Missouri'),
('DDNJ', 'DDNJ', 'Delta Dental of New Jersey'),
('DDPA - Internal', 'DDPA_INTERNAL', 'DDPA Internal Operations'),
('DDPA - National Reporting', 'DDPA_NATIONAL', 'DDPA National Reporting'),
('DDPA - National Tools', 'DDPA_TOOLS', 'DDPA National Tools'),
('DDPA / DDWI / NorthWinds', 'DDPA', 'DDPA, DDWI, and NorthWinds collaboration'),
('DDWA / Triforza', 'DDWA', 'Delta Dental of Washington / Triforza'),
('DDWI', 'DDWI', 'Delta Dental of Wisconsin'),
('NEDD', 'NEDD', 'Northeast Delta Dental'),
('NorthWinds', 'NORTHWINDS', 'NorthWinds');

-- -----------------------------------------------------------------------------
-- 4. USE CASES (Raw CSV data from use_case_list.csv)
-- -----------------------------------------------------------------------------
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

INSERT INTO USE_CASES (MEMBER_COMPANY_OR_AFFILIATION, TYPE, TITLE, DESCRIPTION, VALUE_OR_OUTCOME, KEY_DATA_DOMAINS, CURRENT_STATUS, ANTICIPATED_START_DATE, EST_TSHIRT_SIZE, EST_TIME, PARTNERS) VALUES
('DDCA Group', 'Use Case', 'Business Continuity/DR', 'Business Continuity/Disaster Recovery (BCDR): Replicating Snowflake instance for BCDR.', NULL, 'Compliance', NULL, NULL, NULL, NULL, NULL),
('DDCA Group', 'Use Case', 'Call Center Analytics', 'Train a model call center volume prediction model. Predict call usage, group segmentation.', NULL, 'Operations', NULL, NULL, NULL, NULL, NULL),
('DDCA Group', 'Use Case', 'Operational Reporting', 'Operational Reporting on Snowflake: Current operational reports operating from SQL Server was pulling from multiple instances providing different results. This will provide more accurate reporting from a single view. Snowflake is becoming the central repository, so they are sunsetting operational reporting from other sources.', NULL, 'Operations', NULL, NULL, 'XXL', '12-18 Months', NULL),
('DDCA Group', 'Use Case', 'SQL Server Migration', 'SQL Server Migration: Actuarial DB migration to Snowflake. (Using partner Cloud EQS)', NULL, 'IT', NULL, NULL, 'XXL', '12-18 Months', NULL),
('DDCA Group', 'Use Case', 'Subscriber 360', 'Subscriber 360 - DDCA has replaced legacy on-prem analytical products with Snowflake for all their member data.', NULL, 'Member', NULL, NULL, NULL, NULL, NULL),
('DDCA Group', 'Migration', NULL, 'Projects coming up in 2026. All migrations to Snowflake:
1. EDW Migration (SQL Server).
2. TDV Retirement.
3. Book of Business /Conversion.
4. Non-KPI Actuarial Data Mart - Enterprise Data Platform.
5. ARP migration to Snowflake.
6. IVR migration to Snowflake.', NULL, NULL, 'Implementing', '2H2026 - 2H2027', 'XXL', '12-18 Months', NULL),
('DDIA', 'Migration', 'Initial Snowflake Migration', 'Potential OpenFlow CDC from their own prem application database, land into Snowflake Raw layer, and start conforming/modeling in alignment with NDW.', NULL, 'All', 'Evaluation', '1H2026', 'L', '8 Months', NULL),
('DDID', 'Migration', 'Initial Snowflake Migration', 'DDID does not have an existing on-prem data warehouse. The likely right approach is to use OpenFlow CDC from their own prem application database (ProClaim), land into Snowflake Raw layer, and start conforming/modeling in alignment with NDW.', NULL, 'All', 'Planning', '1H2026', NULL, NULL, NULL),
('DDMI - Group', 'Use Case', 'Anomaly Detection', 'Data Science: Currently a lot of their ML pipelines are not in production. But they do use Snowflake for things like anomaly detection.', NULL, 'Operations', 'Evaluating', NULL, 'M', '6 Months', NULL),
('DDMI Group', 'Use Case', 'Customer Data Platform', 'Customer Data Platform: Using Streamsets to ingest data from On-Prem Oracle databases. Datamarts for their CDP use case are built using Dynamic Tables. They share these marts out via Snowflake Data Sharing.', NULL, 'Member', NULL, NULL, NULL, NULL, NULL),
('DDMI Group', 'Migration', NULL, 'Migration of existing EDW, currently sitting on Oracle Exadata over to Snowflake. Lift and Shift.', NULL, NULL, NULL, '1H2026', NULL, NULL, NULL),
('DDMO', 'Use Case', 'EDI Processing', 'EDI file processing utililty', NULL, 'B&E', 'In Production', NULL, NULL, NULL, NULL),
('DDMO', 'Use Case', 'EDI Processing App', 'EDI file processing app use to ingest/transform large B&E files and enrollment files for stakeholder groups', NULL, 'Operations', 'In Production', NULL, NULL, NULL, NULL),
('DDMO', 'Migration', 'Initial Snowflake Migration', 'DDMO has an existing on-prem SQL Server warehouse. They also use SkyGen. They have begun ETL''s their data from current warehouse and SkyGen into their Snowflake account. Potential hybrid lift and shift and new new Raw/Conform/Model pattern.', NULL, NULL, NULL, '2H2026', NULL, NULL, NULL),
('DDNJ', 'Use Case', 'BigQuery integration', 'DDNJ is heavily invested in BigQuery. Scope of this use case would be to find effective ways to integrate DDNJ BigQuery with DDPA''s NDW', NULL, 'All', 'Idea', NULL, NULL, NULL, NULL),
('DDPA - Internal', 'Use Case', 'AI POC - Company Headquarters', 'POC with Cortex to determine the corporate headquarter state of customer employer groups', NULL, 'Compliance', 'Implementing', NULL, NULL, NULL, NULL),
('DDPA - Internal', 'Use Case', 'AI POC - Provider Credentialing Forms', 'Proof of concept to look at capability to ingest and use Cortex on top several 100 provider credentialing forms for Compliance personnel', NULL, NULL, 'Idea', NULL, NULL, NULL, NULL),
('DDPA - Internal', 'Use Case', 'Centralized Logging', 'Centralizing all application logs for further use including troubleshooting, technical support, driving business insights', NULL, 'Operations', 'In Production', NULL, 'XXL', '12-18 Months', NULL),
('DDPA - Internal', 'Use Case', 'Data Retention', 'Retaining historical data within Snowflake for auditing and archival purposes', NULL, 'Compliance', 'In Production', NULL, 'L', '8 Months', NULL),
('DDPA - Internal', 'Use Case', 'Security Data Lake', NULL, NULL, NULL, 'Evaluating', NULL, NULL, NULL, NULL),
('DDPA - Internal', 'Migration', 'OpenFlow CDC for Oracle', 'OpenFlow CDC Oracle application database. Oracle is currently ingested into Snowflake by Matillion CDC and custom components', NULL, NULL, 'Planning', NULL, 'XXL', '12-18 Months', 'Potentially Squadron'),
('DDPA - Internal', 'Migration', 'OpenFlow CDC for Postgres', 'OpenFlow CDC Postgres application database. Postgres is currently ingested into Snowflake by Matillion.', NULL, NULL, 'Planning', NULL, 'XXL', '12-18 Months', 'Potentially Squadron'),
('DDPA - National Reporting', 'Use Case', 'Actuarial and Underwriting (TIN) Reporting', NULL, NULL, NULL, 'In Production', NULL, NULL, NULL, NULL),
('DDPA - National Reporting', 'Use Case', 'Actuarial and Underwriting Reporting', NULL, NULL, NULL, 'In Production', NULL, NULL, NULL, NULL),
('DDPA - National Reporting', 'Use Case', 'CAHPS Reporting', NULL, NULL, NULL, 'In Production', NULL, NULL, NULL, NULL),
('DDPA - National Reporting', 'Use Case', 'Community Impact Reporting', NULL, NULL, NULL, 'In Production', NULL, NULL, NULL, NULL),
('DDPA - National Reporting', 'Use Case', 'DD.com Opt-In/Opt-Out Reporting', NULL, NULL, NULL, 'In Production', NULL, NULL, NULL, NULL),
('DDPA - National Reporting', 'Use Case', 'Mobile and Portal Reporting', NULL, NULL, NULL, 'In Production', NULL, NULL, NULL, NULL),
('DDPA - National Reporting', 'Use Case', 'Network Management Reporting', NULL, NULL, NULL, 'In Production', NULL, NULL, NULL, NULL),
('DDPA - National Reporting', 'Use Case', 'NPF- Data Integrity Reporting', NULL, NULL, NULL, 'In Production', NULL, NULL, NULL, NULL),
('DDPA - National Reporting', 'Use Case', 'Provider Relations (TIN) Reporting', NULL, NULL, NULL, 'In Production', NULL, NULL, NULL, NULL),
('DDPA - National Reporting', 'Use Case', 'Provider Relations Reporting', NULL, NULL, NULL, 'In Production', NULL, NULL, NULL, NULL),
('DDPA - National Reporting', 'Use Case', 'Sales Insights Reporting', NULL, NULL, NULL, 'In Production', NULL, NULL, NULL, NULL),
('DDPA - National Reporting', 'Use Case', 'System Operations Reporting', NULL, NULL, NULL, 'In Production', NULL, NULL, NULL, NULL),
('DDPA - National Tools', 'Use Case', 'Death Master File', 'Retrive government managed Death Master File to leverage in operations', NULL, 'Operations', 'In Development', NULL, 'L', '8 Months', NULL),
('DDPA - National Tools', 'Use Case', 'Eliminate duplicative marketing', 'Remove current Delta Dental subscribers from mailing lists where they may receive incorrect mailers from other member companies', NULL, 'Marketing', 'In Production', NULL, 'M', '6 Months', NULL),
('DDPA - National Tools', 'Use Case', 'Milliman PPO Study', 'Leverage national claims and membership data to participate in Milliman research study which produces valuable output highlighting Delta Dental''s value in the market', NULL, 'Compliance, Sales', 'In Production', NULL, NULL, NULL, NULL),
('DDPA - National Tools', 'Use Case', 'National Data Warehouse', 'Central repository for all of Delta Dental network data in one place in Snowflake. Member Companies'' data is brought in to unlock a variety of use cases that span across the entire DD network.', NULL, 'Foundation', 'In Production', NULL, NULL, NULL, NULL),
('DDPA - National Tools', 'Use Case', 'OIG Exclusions Database', 'Retrieve gvernment OIG exlusion data to identify bad actors and block from systems', NULL, 'Operations', 'In Production', NULL, NULL, NULL, NULL),
('DDPA - National Tools', 'Use Case', 'Opportunity Database', 'National data aggregation and reporting of sales data to ensure national compliance with Delta Dental membership standards', NULL, 'Compliance', 'In Production', NULL, NULL, NULL, NULL),
('DDPA - National Tools', 'Use Case', 'Network Optimization Tool (DDWI)', 'Intent is to build a Semantic Layer to standardize definitions/metrics across the organization. Enable standardication across claims, eligibility, and provider', NULL, NULL, 'In Development', NULL, NULL, NULL, NULL),
('DDPA / DDWI / NorthWinds', 'Migration', 'OpenFlow CDC for SQL Server', 'OpenFlow CDC SQL Server data warehouse. DDPA currently uses it''s Matillion instance to pull in DDWI/NorthWinds legacy SQL Server wareshouse. Potentially move this to OpenFlow.', NULL, NULL, 'Idea', NULL, NULL, NULL, 'Potentially Squadron'),
('DDWA / Triforza', 'Migration', NULL, 'Migration of existing EDW, currently sitting on SQL Server (need to confirm) over to Snowflake. Lift and Shift.', NULL, NULL, NULL, '2H2026', 'L', '8 Months', NULL),
('DDWI', 'Use Case', 'Network Optimization Tools', 'Tool built/used by DDWI to manage provider network - looking to expand nationally', NULL, 'Provider', 'Implementing', NULL, NULL, NULL, NULL),
('NEDD', 'Migration', 'Initial Snowflake Migration', 'Potential OpenFlow CDC from their own prem application database, land into Snowflake Raw layer, and start conforming/modeling in alignment with NDW.', NULL, 'All', 'Evaluation', '1H2026', 'M', '4-6 Months', NULL),
('NorthWinds', 'Migration', 'KeySpring Data Warehouse', 'Standing up new Snowflake data warehouse extracting data from their Keyspring platform (HealthEdge back end), landing into raw layer and then conforming/modeling. In close partnership with NDW.', NULL, NULL, 'In Development', '2H2026', 'XL', '12 Months', NULL),
('NorthWinds', 'Migration', 'Legacy Data Warehouse', 'Legacy SQL Server warehouse that supports legacy claims system (Advantech). Potential lift and shift opportunity.', NULL, NULL, 'Idea', '2H2026', 'XL', '12 Months', NULL),
('DDMI', 'Use Case', 'Fortifying Data Movement and Observability', 'DDMI currently uses SteamSets for data movement. They do not have a holistic data observability tool', NULL, NULL, 'Idea', NULL, NULL, NULL, NULL),
('DDMI', 'Use Case', 'Optimizing Data Transformation', 'Looking for the best intersection of performance and cost. In Snowflake they are using their own queries plus some DBT. On-prem uses Informatica', NULL, NULL, 'Idea', NULL, NULL, NULL, NULL),
('DDMI', 'Use Case', 'Semantic Layer', NULL, NULL, 'All', 'Idea', NULL, NULL, NULL, NULL),
('DDCA', 'Use Case', 'ADM EDP Ph II Data Federal', NULL, NULL, NULL, NULL, 'CY2026', NULL, NULL, NULL),
('DDCA', 'Use Case', 'Actuarial Direct Usage (Self Service)', NULL, NULL, NULL, NULL, 'CY2026', NULL, NULL, NULL),
('DDCA', 'Use Case', 'EDW Decommision', 'Some reports currently rely on Oracle EDW, most data is already ingested in Snowflake. Praveen outlined a plan to migrate 50-70% of workloads by year-end CY2025, with the remainder to be completed next year, including repointing reports to Snowflake and rebuilding universes', NULL, NULL, 'In Progress', 'Q1 2026', NULL, NULL, NULL),
('DDCA', 'Use Case', 'EDW Decommision Form 5500', NULL, NULL, NULL, 'In Progress', 'Q1 2026', NULL, NULL, NULL),
('DDCA', 'Use Case', 'EDW Decom BOBJ Reports', NULL, NULL, NULL, NULL, 'CY2026', NULL, NULL, NULL),
('DDCA', 'Use Case', 'Skygen (Qlik + Consumption)', NULL, NULL, NULL, NULL, 'CY2026', NULL, NULL, NULL),
('DDCA', 'Use Case', 'PAM API (Pract Location + Term)', 'Practice Management tool', NULL, NULL, NULL, 'CY2026', NULL, NULL, NULL),
('DDCA', 'Use Case', 'Application Track ADM', 'Applications that the data team uses today. Plan to review how applications interact with snowflake. Planning for standardization. Source will be Snowflake', NULL, NULL, 'In Progress', 'CY2026', NULL, NULL, NULL),
('DDCA', 'Use Case', 'Dataiku', 'Models will be run from Snowflake', NULL, NULL, NULL, 'CY2026', NULL, NULL, NULL),
('DDCA', 'Use Case', 'AI Lab', 'Enabling for internal technology team members to do R&D. Not Snowflake specific, there are Azure tools in use too. Opportunity for internal users to develop new processes and patterns', NULL, NULL, 'In Progress', 'CY2026', NULL, NULL, NULL),
('DDCA', 'Use Case', 'BOBJ PBI Conversion', 'Plan to bring real time data into Snowflake. Will point business objects into raw layer. Focus on 30-40% of data this year with effort to continue into 2027', NULL, NULL, 'Planning', 'CY2026', NULL, NULL, NULL),
('DDCA', 'Use Case', 'MSS New User Groups Onboard (Innov DB)', '"Managed Self Service" business stakeholders are given the ability to create reports and query data from Snowflake. Will have need for skilled resources, particularly AI/ML engineers and data modelers, to support these initiatives', NULL, NULL, 'In Progress', 'CY2026', NULL, NULL, NULL),
('DDCA', NULL, 'Data Cloud', NULL, NULL, NULL, NULL, 'CY2026', NULL, NULL, NULL),
('DDCA', 'Use Case', 'Cortex Analyst', 'POC in progress right now to determine capabilities and resulting use cases', NULL, NULL, 'Ideation / In Progress', 'CY2026', NULL, NULL, NULL),
('DDCA', NULL, 'Near Real time replication needs', NULL, NULL, NULL, NULL, 'CY2026', NULL, NULL, NULL),
('DDCA', NULL, 'Semantic Layer', 'Need for a semantic layer to expose data to users through EDP platform, using Calibra for metadata and business glossaries. Concerns about potentially rebuilding semantic models in YAML for Cortex, which would duplicate work already done in JSON for the gold publishing layer.', NULL, NULL, 'Ideation', NULL, NULL, NULL, NULL),
('DDWA / Triforza', 'Use Case', 'Foundational FWA Detection', 'The core migration of the existing SQL EDW to Snowflake. This is the essential first step that establishes the technical bedrock for all future data and AI capabilities.', NULL, NULL, NULL, NULL, 'XXL', NULL, NULL),
('DDWA / Triforza', 'Use Case', 'Data Engineering Automation & Governance', '(Data Platform) Establish robust, automated data ingestion pipelines (e.g., using Fivetran, dbt) and implement a data governance framework (e.g., data catalog, quality checks). This ensures all data on the platform is reliable, trusted, and ready for analytics.', NULL, NULL, NULL, NULL, 'XL', NULL, NULL),
('DDWA / Triforza', 'Use Case', 'Self-Service Analytics Enablement', '(Data) Roll out a governed self-service analytics environment using tools like PowerBI connected to Snowflake. This empowers business users to answer their own questions, reducing the burden on IT and fostering a data-driven culture, mirroring the successful path of DDMI.', NULL, NULL, NULL, NULL, 'L', NULL, NULL),
('DDWA / Triforza', 'Use Case', 'AI-Powered Claims Validation', '(AI/ML) Deploy an AI model to "scrub" claims before submission. The model identifies common errors, missing documentation, or incorrect codes, drastically reducing denial rates and the high cost of rework. This is a high-impact, rapid-ROI application of AI.', NULL, NULL, NULL, NULL, 'XL', NULL, NULL),
('DDWA / Triforza', 'Use Case', 'Provider Network Performance Analytics', '(Analytics) Develop dashboards to analyze provider performance, cost efficiency, and treatment patterns. This provides the data needed to optimize the network, support value-based care initiatives, and manage costs more effectively.', NULL, NULL, NULL, NULL, 'L', NULL, NULL),
('DDWA / Triforza', 'Use Case', 'Foundational FWA Detection', '(AI/ML) Implement an initial Fraud, Waste, and Abuse detection system. This moves beyond simple rules to use anomaly detection and peer-group analysis in Snowflake to flag suspicious billing patterns that were previously undetectable, serving as a precursor to more advanced models.', NULL, NULL, NULL, NULL, 'XL', NULL, NULL),
('DDWA / Triforza', 'Use Case', 'Data Science Platform Setup', '(Data Platform) Establish a dedicated workspace within Snowflake (e.g., Snowpark) for data scientists. This provides the tools and secure environment needed to begin developing and testing the next generation of custom machine learning models.', NULL, NULL, NULL, NULL, 'M', NULL, NULL),
('DDWA / Triforza', 'Use Case', 'Connect to Delta Dental Analytics Hub', '(Data Sharing) A pivotal strategic step. Establish a secure data-sharing connection into the cross-consortium Analytics Hub. This gives DDWA access to national-scale data and advanced models it could not build alone, providing an immense competitive advantage.', NULL, NULL, NULL, NULL, 'XXL', NULL, NULL),
('DDWA / Triforza', 'Use Case', 'Consume Consortium FWA Models', '(AI/ML) Instead of building the most complex AI fraud models from scratch, consume the superior, multi-state FWA models developed by leaders like DDPA/DDCA via the Analytics Hub. This provides top-tier fraud prevention as a service.', NULL, NULL, NULL, NULL, 'L', NULL, NULL),
('DDWA / Triforza', 'Use Case', 'Generative AI for Claims Narrative Summarization', '(AI/ML) Deploy a Generative AI model to read and summarize unstructured text from clinical notes and claim narratives. This provides human adjudicators with a concise summary, dramatically accelerating the review of complex claims.', NULL, NULL, NULL, NULL, 'L', NULL, NULL),
('DDWA / Triforza', 'Use Case', 'Predictive Member Outreach', '(AI/ML) Use machine learning to analyze member data and predict individuals at high risk for lapsing care or declining necessary treatment. This enables proactive, targeted outreach to improve health outcomes and member retention.', NULL, NULL, NULL, NULL, 'M', NULL, NULL),
('DDWA / Triforza', 'Use Case', 'Contribute to National Trends Data Product', '(Data Monetization) Securely contribute de-identified data to the Analytics Hub to support the creation of a national-level data product. This creates a new, non-premium revenue stream for DDWA as a participant in the consortium.', NULL, NULL, NULL, NULL, 'M', NULL, NULL),
('DDWA / Triforza', 'Use Case', 'Develop "Provider Efficiency" Native App', '(Snowflake Native App) (Triforza-led) Build a Snowflake Native App that can be deployed to provider networks. The app could offer AI-powered eligibility verification or automated claim status checks, helping providers reduce their own administrative costs and making DDWA their preferred partner.', NULL, NULL, NULL, NULL, 'XL', NULL, NULL),
('DDWA / Triforza', 'Use Case', 'Real-Time Insurance Verification API', '(Data Engineering) (Triforza-led) Develop a real-time API that allows provider offices to instantly verify patient eligibility and benefits directly from their own systems. This reduces administrative friction and dramatically improves the provider experience', NULL, NULL, NULL, NULL, 'L', NULL, NULL);

-- -----------------------------------------------------------------------------
-- 5. VIEW: USE CASES WITH COMPANY INFO (Mapping view)
-- -----------------------------------------------------------------------------
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

-- -----------------------------------------------------------------------------
-- 6. CONTACTS
-- -----------------------------------------------------------------------------
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

-- -----------------------------------------------------------------------------
-- 7. CONTACT SUBCOMMITTEES (Many-to-many)
-- -----------------------------------------------------------------------------
CREATE OR REPLACE TABLE CONTACT_SUBCOMMITTEES (
    CONTACT_ID VARCHAR(20) REFERENCES CONTACTS(CONTACT_ID),
    SUBCOMMITTEE VARCHAR(50),
    PRIMARY KEY (CONTACT_ID, SUBCOMMITTEE)
);

-- -----------------------------------------------------------------------------
-- 8. MEETINGS
-- -----------------------------------------------------------------------------
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

-- -----------------------------------------------------------------------------
-- 9. MONTHLY SPEND
-- -----------------------------------------------------------------------------
CREATE OR REPLACE TABLE MONTHLY_SPEND (
    MONTH_KEY VARCHAR(7) NOT NULL,
    COMPANY_ID VARCHAR(20) REFERENCES COMPANIES(COMPANY_ID),
    SPEND_AMOUNT_K NUMBER(10,2),
    PRIMARY KEY (MONTH_KEY, COMPANY_ID)
);

-- -----------------------------------------------------------------------------
-- 10. INVESTMENTS
-- -----------------------------------------------------------------------------
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

-- -----------------------------------------------------------------------------
-- 11. MARKETPLACE DRAWDOWNS
-- -----------------------------------------------------------------------------
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

-- -----------------------------------------------------------------------------
-- 12. PARTNERS
-- -----------------------------------------------------------------------------
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

-- -----------------------------------------------------------------------------
-- 13. REFERENCE TABLES
-- -----------------------------------------------------------------------------
CREATE OR REPLACE TABLE REF_STATUSES (
    STATUS VARCHAR(50) PRIMARY KEY,
    SORT_ORDER NUMBER,
    STATUS_TYPE VARCHAR(20)
);

INSERT INTO REF_STATUSES (STATUS, SORT_ORDER, STATUS_TYPE) VALUES
('Idea', 1, 'USE_CASE'),
('Evaluation', 2, 'USE_CASE'),
('Evaluating', 2, 'USE_CASE'),
('Planning', 3, 'USE_CASE'),
('In Development', 4, 'USE_CASE'),
('In Progress', 5, 'USE_CASE'),
('Implementing', 5, 'USE_CASE'),
('In Production', 6, 'USE_CASE'),
('Completed', 7, 'USE_CASE'),
('On Hold', 8, 'USE_CASE'),
('Cancelled', 9, 'USE_CASE'),
('Ideation / In Progress', 5, 'USE_CASE');

CREATE OR REPLACE TABLE REF_TSHIRT_SIZES (
    SIZE_CODE VARCHAR(10) PRIMARY KEY,
    SIZE_NAME VARCHAR(20),
    SORT_ORDER NUMBER,
    TYPICAL_DURATION VARCHAR(50)
);

INSERT INTO REF_TSHIRT_SIZES (SIZE_CODE, SIZE_NAME, SORT_ORDER, TYPICAL_DURATION) VALUES
('S', 'Small', 1, '1-2 Months'),
('M', 'Medium', 2, '4-6 Months'),
('L', 'Large', 3, '6-8 Months'),
('XL', 'Extra Large', 4, '9-12 Months'),
('XXL', 'Extra Extra Large', 5, '12-18 Months');

CREATE OR REPLACE TABLE REF_DATA_DOMAINS (
    DOMAIN VARCHAR(50) PRIMARY KEY,
    DESCRIPTION VARCHAR(200)
);

INSERT INTO REF_DATA_DOMAINS (DOMAIN, DESCRIPTION) VALUES
('All', 'All data domains'),
('B&E', 'Benefits and Eligibility'),
('Compliance', 'Regulatory and compliance data'),
('Foundation', 'Foundational/infrastructure data'),
('IT', 'Information Technology'),
('Marketing', 'Marketing and outreach data'),
('Member', 'Member/subscriber data'),
('Operations', 'Operational data'),
('Provider', 'Provider network data'),
('Sales', 'Sales and revenue data');

CREATE OR REPLACE TABLE REF_GOVERNANCE_TIERS (
    TIER_KEY VARCHAR(30) PRIMARY KEY,
    TIER_NAME VARCHAR(100),
    DESCRIPTION TEXT,
    CADENCE VARCHAR(50)
);

INSERT INTO REF_GOVERNANCE_TIERS (TIER_KEY, TIER_NAME, DESCRIPTION, CADENCE) VALUES
('operations_work_group', 'Umbrella Deal Operations Work Group', 'Monitor Snowflake spend, provide direction on investment spend, and general oversight', 'Monthly (moving to Quarterly)'),
('steering_committee', 'Snowflake Steering Committee', 'Provide strategic oversight and guidance to all member companies leveraging Snowflake', 'Monthly'),
('user_community', 'Snowflake User Community', 'Ongoing education, hands-on labs, workshops aligned to member company priorities', 'Monthly/Bi-Monthly');

-- -----------------------------------------------------------------------------
-- 14. SUMMARY VIEWS
-- -----------------------------------------------------------------------------

-- View: Company coverage by operating area
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

-- View: Use case summary by company
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

-- View: Use case summary by status
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
-- END OF DDL SCRIPT
-- =============================================================================
