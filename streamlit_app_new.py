import streamlit as st
import json
from snowflake.snowpark.context import get_active_session

# Get the active Snowflake session for Streamlit in Snowflake
session = get_active_session()

# App configuration
st.set_page_config(
    page_title="Cigna Claims Optimization System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and header
st.title("🏥 Cigna Claims Optimization System")
st.markdown("**Powered by Snowflake Cortex Dual-Agent AI**")
st.markdown("---")

# Sidebar for navigation
st.sidebar.title("📋 Workflow Steps")
st.sidebar.markdown("""
1. **Select Patient** 
2. **Choose Procedure**
3. **Enter Clinical Notes**
4. **Generate Claim** (Builder Agent)
5. **Insurance Case** (Insurance Agent)
6. **Judge Decision** (AI Arbitrator)
7. **Appeals Process** (If needed)
8. **Final Decision**
""")

# Initialize session state
if 'workflow_step' not in st.session_state:
    st.session_state.workflow_step = 1
if 'generated_claim' not in st.session_state:
    st.session_state.generated_claim = None
if 'insurance_rebuttal' not in st.session_state:
    st.session_state.insurance_rebuttal = None
if 'judge_decision' not in st.session_state:
    st.session_state.judge_decision = None
if 'appeals_round' not in st.session_state:
    st.session_state.appeals_round = 0
if 'final_decision' not in st.session_state:
    st.session_state.final_decision = None

# Helper function to load patients
@st.cache
def load_patients():
    """Load all Cigna patients from database"""
    query = "SELECT PATIENT_ID, FIRST_NAME, LAST_NAME, MEDICAL_HISTORY_SUMMARY, INSURANCE_PROVIDER, POLICY_NUMBER FROM CLAIMS_DEMO.PUBLIC.PATIENTS ORDER BY PATIENT_ID"
    result = session.sql(query).collect()
    return [(row['PATIENT_ID'], f"{row['FIRST_NAME']} {row['LAST_NAME']}", row['MEDICAL_HISTORY_SUMMARY'], row['POLICY_NUMBER']) 
            for row in result]

# Helper function to load procedures  
@st.cache
def load_procedures():
    """Load common medical procedures"""
    query = "SELECT PROCEDURE_CODE, PROCEDURE_NAME, CIGNA_COVERAGE_NOTES FROM CLAIMS_DEMO.PUBLIC.COMMON_PROCEDURES ORDER BY PROCEDURE_CODE"
    result = session.sql(query).collect()
    return [(row['PROCEDURE_CODE'], row['PROCEDURE_NAME'], row['CIGNA_COVERAGE_NOTES']) for row in result]

# Main workflow
st.header("🏥 Provider Claim Workflow")

# Step 1: Select Patient
st.subheader("1. 👤 Select Patient")

patients = load_patients()
patient_options = [f"{pid} - {name} (Policy: {policy})" for pid, name, history, policy in patients]

selected_patient = st.selectbox(
    "Choose Cigna Patient:",
    options=patient_options,
    help="Select a patient from the Cigna member database"
)

if selected_patient:
    patient_id = selected_patient.split(' - ')[0]
    patient_info = next(p for p in patients if p[0] == patient_id)
    
    with st.expander("📋 Patient Medical History"):
        st.write(f"**Patient ID:** {patient_info[0]}")
        st.write(f"**Name:** {patient_info[1]}")
        st.write(f"**Policy Number:** {patient_info[3]}")
        st.write(f"**Medical History:** {patient_info[2]}")

# Step 2: Select Procedure
if selected_patient:
    st.subheader("2. 🏥 Select Procedure")
    
    procedures = load_procedures()
    procedure_options = [f"{code} - {name}" for code, name, notes in procedures]
    
    selected_procedure = st.selectbox(
        "Choose Medical Procedure:",
        options=procedure_options,
        help="Select the medical procedure for this claim"
    )
    
    if selected_procedure:
        procedure_code = selected_procedure.split(' - ')[0]
        procedure_info = next(p for p in procedures if p[0] == procedure_code)
        
        with st.expander("📝 Cigna Coverage Information"):
            st.write(f"**Procedure Code:** {procedure_info[0]}")
            st.write(f"**Procedure Name:** {procedure_info[1]}")
            st.write(f"**Cigna Coverage Notes:** {procedure_info[2]}")

# Step 3: Clinical Notes
if selected_patient and selected_procedure:
    st.subheader("3. 📝 Enter Clinical Notes")
    
    clinical_notes = st.text_area(
        "Clinical Notes and Justification:",
        height=150,
        help="Enter detailed clinical notes explaining the medical necessity of the procedure",
        placeholder="Patient presents with symptoms requiring the selected procedure. Medical history indicates..."
    )
    
    # Generate Claim Button
    st.markdown("---")
    if st.button("🔄 Generate Optimized Claim", type="primary", use_container_width=True):
        if clinical_notes.strip():
            st.session_state.workflow_step = 2
            st.experimental_rerun()
        else:
            st.error("Please enter clinical notes before generating claim")

# Step 4: Builder Agent - Claim Generation
if st.session_state.workflow_step >= 2 and selected_patient and selected_procedure and clinical_notes:
    st.subheader("4. 🤖 Builder Agent - Generating Claim")
    
    if not st.session_state.generated_claim:
        with st.spinner("Builder Agent generating optimized claim..."):
            try:
                # Call Builder Agent function
                builder_query = f"""
                SELECT CLAIMS_DEMO.PUBLIC.BUILDER_AGENT(
                    '{patient_id}',
                    '{procedure_code}',
                    '{clinical_notes.replace("'", "''")}'
                ) as GENERATED_CLAIM
                """
                
                builder_result = session.sql(builder_query).collect()
                generated_claim = builder_result[0]['GENERATED_CLAIM']
                st.session_state.generated_claim = generated_claim
                
                st.success("✅ Claim Generated Successfully!")
                st.session_state.workflow_step = 3
                
            except Exception as e:
                st.error(f"Error generating claim: {str(e)}")
    
    if st.session_state.generated_claim:
        # Display the generated claim
        try:
            claim_json = json.loads(st.session_state.generated_claim)
            st.json(claim_json, expanded=False)
        except json.JSONDecodeError:
            st.warning("Claim is not in valid JSON format")
            st.text(st.session_state.generated_claim)

# Step 5: Insurance Agent - Building Their Case
if st.session_state.workflow_step >= 3 and st.session_state.generated_claim:
    st.subheader("5. 🛡️ Insurance Agent - Building Case Presentation")
    
    if not st.session_state.insurance_rebuttal:
        with st.spinner("Insurance Agent analyzing claim..."):
            try:
                # Call Insurance Agent function with policy integration
                insurance_query = f"""
                SELECT CLAIMS_DEMO.PUBLIC.INSURANCE_AGENT_WITH_POLICY(
                    '{st.session_state.generated_claim.replace("'", "''")}',
                    '{procedure_code}'
                ) as INSURANCE_REBUTTAL
                """
                
                insurance_result = session.sql(insurance_query).collect()
                insurance_rebuttal = insurance_result[0]['INSURANCE_REBUTTAL']
                st.session_state.insurance_rebuttal = insurance_rebuttal
                st.session_state.workflow_step = 5
                
            except Exception as e:
                st.error(f"Error analyzing claim: {str(e)}")
                
    if st.session_state.insurance_rebuttal:
        # Parse and display insurance analysis
        try:
            rebuttal_json = json.loads(st.session_state.insurance_rebuttal)
            
            # Extract key metrics
            strength_score = rebuttal_json.get('strength_score', 0)
            rebuttal_summary = rebuttal_json.get('rebuttal_summary', 'No summary provided')
            denial_reasons = rebuttal_json.get('denial_reasons', [])
            policy_citations = rebuttal_json.get('policy_citations', [])
            
            # Display Insurance Agent's case presentation (no final decision)
            st.markdown("**Insurance Agent Case Analysis:**")
            st.markdown(f"**Case Assessment Score:** {strength_score:.2f}/1.0")
            st.markdown(f"**Summary:** {rebuttal_summary}")
            
            if denial_reasons:
                st.markdown("**Potential Issues Identified:**")
                for reason in denial_reasons:
                    st.markdown(f"• {reason}")
            
            # Display policy references
            if policy_citations:
                st.markdown("**Supporting Policy Citations:**")
                for citation in policy_citations:
                    st.markdown(f"• {citation}")
            
            # Show full insurance case details
            with st.expander("🔍 Detailed Insurance Agent Case"):
                st.json(rebuttal_json)
        
        except json.JSONDecodeError:
            st.warning("Insurance Agent response is not valid JSON format")
            st.text(st.session_state.insurance_rebuttal)

# Step 6: Judge Decision (AI Arbitrator)
if st.session_state.workflow_step >= 5 and st.session_state.insurance_rebuttal:
    st.markdown("---")
    st.subheader("6. ⚖️ AI Judge - Final Decision")
    
    if not st.session_state.judge_decision:
        if st.button("⚖️ Generate Judge Decision", type="primary", use_container_width=True):
            with st.spinner("AI Judge analyzing both sides..."):
                try:
                    # Call AI Judge function to make final decision
                    judge_query = f"""
                    SELECT CLAIMS_DEMO.PUBLIC.GENERATE_PROVIDER_RECOMMENDATION(
                        '{st.session_state.generated_claim.replace("'", "''")}',
                        '{st.session_state.insurance_rebuttal.replace("'", "''")}',
                        '{patient_id}',
                        '{procedure_code}'
                    ) as JUDGE_DECISION
                    """
                    
                    judge_result = session.sql(judge_query).collect()
                    judge_decision = judge_result[0]['JUDGE_DECISION']
                    st.session_state.judge_decision = judge_decision
                    st.session_state.workflow_step = 6
                    st.experimental_rerun()
                    
                except Exception as e:
                    st.error(f"Error generating judge decision: {str(e)}")
    
    if st.session_state.judge_decision:
        try:
            judge_json = json.loads(st.session_state.judge_decision)
            decision = judge_json.get('final_decision', 'UNKNOWN')
            reasoning = judge_json.get('reasoning', 'No reasoning provided')
            confidence = judge_json.get('confidence_score', 0.0)
            
            # Display judge decision
            if decision.upper() == 'APPROVED':
                st.success(f"✅ **JUDGE DECISION: APPROVED** (Confidence: {confidence:.2f})")
            else:
                st.error(f"❌ **JUDGE DECISION: DENIED** (Confidence: {confidence:.2f})")
            
            st.markdown(f"**Reasoning:** {reasoning}")
            
            with st.expander("🔍 Full Judge Analysis"):
                st.json(judge_json)
            
            st.session_state.final_decision = decision
            
        except json.JSONDecodeError:
            st.warning("Judge decision is not in valid JSON format")
            st.text(st.session_state.judge_decision)

# Step 7: Appeals Process
if st.session_state.workflow_step >= 6 and st.session_state.final_decision:
    st.markdown("---")
    st.subheader("7. ⚖️ Appeals Process")
    
    if st.session_state.appeals_round < 3:  # Maximum 3 appeals rounds
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button(f"📋 Doctor Appeals (Round {st.session_state.appeals_round + 1})", use_container_width=True):
                st.session_state.appeals_round += 1
                st.info(f"Doctor has filed Appeal Round {st.session_state.appeals_round}")
                # Here you could implement actual appeal logic
                
        with col2:
            if st.button(f"🛡️ Insurance Counter-Appeal (Round {st.session_state.appeals_round + 1})", use_container_width=True):
                st.session_state.appeals_round += 1
                st.info(f"Insurance has filed Counter-Appeal Round {st.session_state.appeals_round}")
                # Here you could implement actual counter-appeal logic
    
    else:
        st.warning("⚠️ Maximum appeals rounds reached (3). Final decision stands.")

# Workflow Insights & Supporting Data
if st.session_state.workflow_step >= 3:
    st.markdown("---")
    st.header("📊 Workflow Insights & Supporting Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🧠 Thinking Steps")
        st.markdown("""
        **Agent Workflow Process:**
        1. **Builder Agent** - Gathers patient data, procedure info, and clinical notes
        2. **Data Integration** - Merges with insurance policy and medical history
        3. **Claim Generation** - Creates structured JSON claim using AI reasoning
        4. **Insurance Analysis** - Reviews claim against policy documents and precedents  
        5. **Case Presentation** - Insurance agent builds argument (not decision)
        6. **AI Judge** - Independent arbitrator weighing both sides
        7. **Appeals** - Iterative back-and-forth if parties disagree
        8. **Final Decision** - Binding determination after appeals
        """)
    
    with col2:
        st.subheader("📋 Supporting Tables Used")
        with st.expander("View Database Tables"):
            st.markdown("""
            **Core Data Tables:**
            - `PATIENTS` - Cigna member demographics & medical history
            - `PROCEDURE_CODES_REFERENCE` - Standard medical procedures
            - `DIAGNOSIS_CODES_REFERENCE` - ICD-10 diagnostic codes
            - `CIGNA_POLICY_DOCUMENTS` - Insurance policy text for search
            - `DENIAL_PATTERNS` - Historical denial analysis
            - `SUCCESSFUL_CLAIMS_PATTERNS` - Approval precedents
            
            **Agent Functions:**
            - `BUILDER_AGENT` - Claim generation
            - `INSURANCE_AGENT_WITH_POLICY` - Policy-based analysis  
            - `GENERATE_PROVIDER_RECOMMENDATION` - AI judge decisions
            - `BUILDER_AGENT_OPTIMIZE` - Iterative improvement
            """)

# System Status Dashboard
if st.session_state.workflow_step >= 3:
    st.markdown("---")
    st.header("📊 System Status Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Workflow Step", st.session_state.workflow_step, "of 8")
    
    with col2:
        claim_status = "✅ Generated" if st.session_state.generated_claim else "❌ Pending"
        st.metric("Claim Status", claim_status)
    
    with col3:
        insurance_status = "✅ Analyzed" if st.session_state.insurance_rebuttal else "❌ Pending" 
        st.metric("Insurance Review", insurance_status)
    
    with col4:
        appeals_status = f"Round {st.session_state.appeals_round}/3"
        st.metric("Appeals", appeals_status)
    
    # Reset workflow button
    if st.button("🔄 Reset Workflow", use_container_width=True):
        st.session_state.workflow_step = 1
        st.session_state.generated_claim = None
        st.session_state.insurance_rebuttal = None
        st.session_state.judge_decision = None
        st.session_state.appeals_round = 0
        st.session_state.final_decision = None
        st.experimental_rerun()
