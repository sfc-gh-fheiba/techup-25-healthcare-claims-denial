# 🚀 Streamlit App Deployment Guide

This guide explains how to deploy the Cigna Claims Optimization Streamlit app in Snowflake.

## Prerequisites

- Completed all setup notebooks (01-06)
- Dual-agent system working and tested
- Access to `CLAIMS_DEMO` database with all tables/functions
- Streamlit in Snowflake enabled

## Deployment Steps

### Step 1: Verify System Readiness

Run this query to ensure everything is ready:

```sql
-- System readiness check
SELECT 
    'PATIENTS' as COMPONENT, COUNT(*) as COUNT FROM CLAIMS_DEMO.PUBLIC.PATIENTS
UNION ALL
SELECT 'AGENTS', COUNT(*) FROM CLAIMS_DEMO.PUBLIC.CORTEX_AGENTS_REGISTRY  
UNION ALL
SELECT 'POLICIES', COUNT(*) FROM CLAIMS_DEMO.PUBLIC.CIGNA_POLICY_DOCUMENTS
UNION ALL
SELECT 'FUNCTIONS', COUNT(*) FROM CLAIMS_DEMO.INFORMATION_SCHEMA.FUNCTIONS 
WHERE function_schema = 'PUBLIC' AND function_name LIKE '%AGENT%';
```

**Expected Results:**
- PATIENTS: 5
- AGENTS: 2  
- POLICIES: 3
- FUNCTIONS: 3+

### Step 2: Create Streamlit Stage

```sql
-- Create stage for app files
CREATE STAGE IF NOT EXISTS CLAIMS_DEMO.PUBLIC.STREAMLIT_STAGE;
```

### Step 3: Upload App Files

#### Option A: Using Snowflake Web UI
1. Go to **Data** → **Databases** → **CLAIMS_DEMO** → **PUBLIC** → **Stages** → **STREAMLIT_STAGE**
2. Upload these files:
   - `streamlit_app.py`
   - `requirements.txt` 
   - `environment.yml`
   - `.streamlit/config.toml`

#### Option B: Using SnowSQL
```bash
# Upload files to stage
PUT file://streamlit_app.py @CLAIMS_DEMO.PUBLIC.STREAMLIT_STAGE overwrite=true;
PUT file://requirements.txt @CLAIMS_DEMO.PUBLIC.STREAMLIT_STAGE overwrite=true;
PUT file://environment.yml @CLAIMS_DEMO.PUBLIC.STREAMLIT_STAGE overwrite=true;
PUT file://.streamlit/config.toml @CLAIMS_DEMO.PUBLIC.STREAMLIT_STAGE/.streamlit/ overwrite=true;
```

### Step 4: Create Streamlit App

```sql
-- Deploy Streamlit app
CREATE OR REPLACE STREAMLIT CLAIMS_DEMO.PUBLIC.CIGNA_CLAIMS_OPTIMIZATION_APP
ROOT_LOCATION = '@CLAIMS_DEMO.PUBLIC.STREAMLIT_STAGE'
MAIN_FILE = 'streamlit_app.py'
QUERY_WAREHOUSE = 'DEMO_WH';
```

### Step 5: Access Your App

```sql
-- Get app details and URL
DESC STREAMLIT CLAIMS_DEMO.PUBLIC.CIGNA_CLAIMS_OPTIMIZATION_APP;

-- Verify deployment
SHOW STREAMLITS IN SCHEMA CLAIMS_DEMO.PUBLIC;
```

The app URL will be displayed - click to access your deployed app!

## App Features

### 🔹 **Provider Interface**
- **Patient Selection**: Choose from 5 Cigna members
- **Procedure Selection**: Pick from 8 common procedures
- **Clinical Notes**: Enter medical necessity and symptoms
- **Real-time Validation**: Instant feedback on inputs

### 🔹 **Dual-Agent Workflow**
- **Builder Agent**: Generates structured JSON insurance claims
- **Insurance Agent**: Provides policy-backed rebuttals with strength scores
- **Live Visualization**: Watch agents interact in real-time
- **Optimization Loop**: Iterative claim improvement

### 🔹 **Results Dashboard**
- **Strength Scoring**: 0.0-1.0 scale with color coding
- **Policy Citations**: Specific Cigna policy sections referenced
- **Recommendations**: PROCEED/OPTIMIZE/RECONSIDER guidance
- **Export Options**: Download optimized claims

## Demo Scenarios

### Scenario 1: Routine Lab Work
- **Patient**: John Smith (PAT_001) - Diabetes + Hypertension
- **Procedure**: 85025 (CBC)
- **Clinical**: "Annual wellness screening for diabetes monitoring"
- **Expected**: High approval probability

### Scenario 2: Emergency Care
- **Patient**: Maria Garcia (PAT_002) - Knee surgery history  
- **Procedure**: 99283 (ED Visit)
- **Clinical**: "Severe knee pain after fall, unable to bear weight"
- **Expected**: Emergency coverage, no prior auth needed

### Scenario 3: Cardiology Services
- **Patient**: Thomas Anderson (PAT_005) - Heart disease
- **Procedure**: 93005 (EKG)
- **Clinical**: "Chest discomfort, palpitations, cardiac screening needed"
- **Expected**: Prior authorization required

## Troubleshooting

### Common Issues

**App won't start:**
- Verify all setup notebooks completed
- Check warehouse `DEMO_WH` is active
- Ensure database access permissions

**Agent functions not found:**
- Run notebooks 03-06 to create agent functions
- Verify functions exist: `SHOW FUNCTIONS LIKE '%AGENT%'`

**No policy integration:**
- Run notebook 05 to create policy documents
- Verify Cortex Search service: `SHOW CORTEX SEARCH SERVICES`

**JSON parsing errors:**
- Check agent output format
- Verify agents return valid JSON
- Test agents individually before running app

## Sales Engineer Talking Points

### 🎯 **Snowflake Value Proposition**
- **Single Platform**: Everything runs natively in Snowflake
- **No Data Movement**: Marketplace data + AI + app in one place
- **Enterprise Security**: Healthcare data never leaves Snowflake
- **Instant Scalability**: Auto-scaling compute for any load

### 🤖 **AI Capabilities Showcase**
- **Cortex Complete**: Dual LLM agents with specialized prompts
- **Cortex Search**: Semantic policy search and citations
- **Marketplace Data**: Real healthcare claims powering decisions
- **Structured AI**: JSON-enforced outputs for reliable integration

### 💼 **Business Benefits**
- **Reduced Denials**: AI optimization before submission
- **Faster Processing**: Real-time claim generation and analysis
- **Policy Compliance**: Automatic Cigna policy checking
- **Cost Savings**: Fewer denied claims = improved revenue

---

**Your Cigna Claims Optimization System is ready for live demos!** 🎉
