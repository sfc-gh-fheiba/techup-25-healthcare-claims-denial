-- Streamlit Deployment Script for Snowflake
-- Run this in Snowflake to deploy the Claims Optimization app

-- 1. Create Streamlit app in Snowflake
CREATE OR REPLACE STREAMLIT CLAIMS_DEMO.PUBLIC.CIGNA_CLAIMS_OPTIMIZATION_APP
ROOT_LOCATION = '@CLAIMS_DEMO.PUBLIC.STREAMLIT_STAGE'
MAIN_FILE = 'streamlit_app.py'
QUERY_WAREHOUSE = 'DEMO_WH';

-- 2. Create stage for Streamlit files (if not exists)
CREATE STAGE IF NOT EXISTS CLAIMS_DEMO.PUBLIC.STREAMLIT_STAGE;

-- 3. Upload files to stage (run these commands in SnowSQL or upload via UI)
-- PUT file://streamlit_app.py @CLAIMS_DEMO.PUBLIC.STREAMLIT_STAGE overwrite=true;
-- PUT file://requirements.txt @CLAIMS_DEMO.PUBLIC.STREAMLIT_STAGE overwrite=true;
-- PUT file://environment.yml @CLAIMS_DEMO.PUBLIC.STREAMLIT_STAGE overwrite=true;

-- 4. Verify deployment
SHOW STREAMLITS IN SCHEMA CLAIMS_DEMO.PUBLIC;

-- 5. Get app URL (will be displayed after creation)
DESC STREAMLIT CLAIMS_DEMO.PUBLIC.CIGNA_CLAIMS_OPTIMIZATION_APP;
