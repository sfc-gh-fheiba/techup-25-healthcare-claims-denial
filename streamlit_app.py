import streamlit as st
import json
import plotly.express as px
import plotly.graph_objects as go
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
if 'appeal_history' not in st.session_state:
    st.session_state.appeal_history = []

# Helper function to load patients
@st.cache_data
def load_patients():
    """Load all Cigna patients from database"""
    query = "SELECT PATIENT_ID, FIRST_NAME, LAST_NAME, MEDICAL_HISTORY_SUMMARY, INSURANCE_PROVIDER, POLICY_NUMBER FROM CLAIMS_DEMO.PUBLIC.PATIENTS ORDER BY PATIENT_ID"
    result = session.sql(query).collect()
    return [(row['PATIENT_ID'], f"{row['FIRST_NAME']} {row['LAST_NAME']}", row['MEDICAL_HISTORY_SUMMARY'], row['POLICY_NUMBER']) 
            for row in result]

# Helper function to load procedures  
@st.cache_data
def load_procedures():
    """Load common medical procedures"""
    query = "SELECT PROCEDURE_CODE, PROCEDURE_NAME, CIGNA_COVERAGE_NOTES FROM CLAIMS_DEMO.PUBLIC.COMMON_PROCEDURES ORDER BY PROCEDURE_CODE"
    result = session.sql(query).collect()
    return [(row['PROCEDURE_CODE'], row['PROCEDURE_NAME'], row['CIGNA_COVERAGE_NOTES']) for row in result]

# Enhanced System Dashboard (moved to top)
st.header("📊 Live System Dashboard")

# Create dashboard metrics and visualizations
if st.session_state.workflow_step >= 1:
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

# Enhanced visualizations with Plotly
if st.session_state.workflow_step >= 3:
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        # Workflow Progress Chart
        workflow_steps = ['Patient', 'Procedure', 'Notes', 'Claim Gen', 'Insurance', 'Judge', 'Appeals', 'Final']
        progress = [1 if i < st.session_state.workflow_step else 0 for i in range(len(workflow_steps))]
        
        fig_progress = px.bar(
            x=workflow_steps, 
            y=progress,
            title="🚀 Workflow Progress",
            color=progress,
            color_continuous_scale=['lightgray', 'green']
        )
        fig_progress.update_layout(showlegend=False, height=300)
        st.plotly_chart(fig_progress, use_container_width=True)
    
    with chart_col2:
        # Claim Strength Analysis
        if st.session_state.insurance_rebuttal:
            try:
                rebuttal_json = json.loads(st.session_state.insurance_rebuttal)
                strength_score = rebuttal_json.get('strength_score', 0)
                
                # Create gauge chart for claim strength
                fig_gauge = go.Figure(go.Indicator(
                    mode = "gauge+number+delta",
                    value = strength_score,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "🎯 Claim Strength Score"},
                    delta = {'reference': 0.5},
                    gauge = {
                        'axis': {'range': [None, 1]},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [0, 0.4], 'color': "lightgray"},
                            {'range': [0.4, 0.7], 'color': "yellow"},
                            {'range': [0.7, 1], 'color': "green"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 0.7
                        }
                    }
                ))
                fig_gauge.update_layout(height=300)
                st.plotly_chart(fig_gauge, use_container_width=True)
            except:
                st.info("Claim strength will appear after orchestration")
        else:
            st.info("📊 Claim analysis will appear after orchestration")

# System Stats Overview
if st.session_state.workflow_step >= 1:
    with st.expander("📈 System Statistics"):
        stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
        
        with stat_col1:
            st.metric("👥 Patients", "5", help="Cigna members available")
        with stat_col2:
            st.metric("🏥 Procedures", "8", help="Common procedures loaded")
        with stat_col3:
            st.metric("📋 Policies", "3", help="Cigna policy documents")
        with stat_col4:
            st.metric("🤖 AI Agents", "3", help="Builder + Insurance + Judge")

st.markdown("---")

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
    
    # Dual-Agent Orchestration Button
    st.markdown("---")
    if st.button("🔄 Run Dual-Agent Orchestration Loop", type="primary", use_container_width=True):
        if clinical_notes.strip():
            # Run the complete orchestration loop
            with st.spinner("🤖 Running Dual-Agent Orchestration Loop..."):
                try:
                    # Step 1: Builder Agent - Generate Claim
                    st.info("Step 1: 🤖 Builder Agent generating claim...")
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
                    st.session_state.workflow_step = 4
                    
                    # Step 2: Insurance Agent - Analyze Claim
                    st.info("Step 2: 🛡️ Insurance Agent analyzing claim...")
                    insurance_query = f"""
                    SELECT CLAIMS_DEMO.PUBLIC.INSURANCE_AGENT_WITH_POLICY(
                        '{generated_claim.replace("'", "''")}',
                        '{procedure_code}'
                    ) as INSURANCE_REBUTTAL
                    """
                    
                    insurance_result = session.sql(insurance_query).collect()
                    insurance_rebuttal = insurance_result[0]['INSURANCE_REBUTTAL']
                    st.session_state.insurance_rebuttal = insurance_rebuttal
                    st.session_state.workflow_step = 5
                    
                    # Step 3: AI Judge - Make Decision
                    st.info("Step 3: ⚖️ AI Judge making decision...")
                    judge_query = f"""
                    SELECT CLAIMS_DEMO.PUBLIC.AI_JUDGE_DECISION(
                        '{generated_claim.replace("'", "''")}',
                        '{insurance_rebuttal.replace("'", "''")}',
                        '{patient_id}',
                        '{procedure_code}'
                    ) as JUDGE_DECISION
                    """
                    
                    judge_result = session.sql(judge_query).collect()
                    judge_decision = judge_result[0]['JUDGE_DECISION']
                    st.session_state.judge_decision = judge_decision
                    st.session_state.workflow_step = 6
                    
                    # Parse judge decision to check if denied
                    try:
                        judge_json = json.loads(judge_decision)
                        final_decision = judge_json.get('final_decision', 'UNKNOWN').upper()
                        st.session_state.final_decision = final_decision
                        
                        # Step 4: Appeals Process (if denied)
                        if final_decision == 'DENIED':
                            st.info("Claim denied - Starting appeals process...")
                            st.session_state.appeals_round = 0
                            st.session_state.appeal_history = []
                            
                            # Run appeals loop (max 3 rounds)
                            for round_num in range(1, 4):  # 3 rounds max
                                # Doctor Appeal
                                st.info(f"Step 4.{round_num}a: 📋 Doctor filing appeal round {round_num}...")
                                appeal_query = f"""
                                SELECT CLAIMS_DEMO.PUBLIC.DOCTOR_APPEAL_GENERATOR(
                                    '{generated_claim.replace("'", "''")}',
                                    '{insurance_rebuttal.replace("'", "''")}',
                                    '{judge_decision.replace("'", "''")}',
                                    {round_num}
                                ) as DOCTOR_APPEAL
                                """
                                
                                appeal_result = session.sql(appeal_query).collect()
                                doctor_appeal = appeal_result[0]['DOCTOR_APPEAL']
                                
                                st.session_state.appeals_round = round_num
                                st.session_state.appeal_history.append({
                                    'round': round_num,
                                    'type': 'DOCTOR_APPEAL',
                                    'content': doctor_appeal
                                })
                                
                                # Insurance Counter-Appeal
                                st.info(f"Step 4.{round_num}b: 🛡️ Insurance counter-appeal round {round_num}...")
                                counter_query = f"""
                                SELECT CLAIMS_DEMO.PUBLIC.INSURANCE_COUNTER_APPEAL(
                                    '{doctor_appeal.replace("'", "''")}',
                                    '{insurance_rebuttal.replace("'", "''")}',
                                    {round_num}
                                ) as INSURANCE_COUNTER
                                """
                                
                                counter_result = session.sql(counter_query).collect()
                                insurance_counter = counter_result[0]['INSURANCE_COUNTER']
                                
                                st.session_state.appeal_history.append({
                                    'round': round_num,
                                    'type': 'INSURANCE_COUNTER',
                                    'content': insurance_counter
                                })
                        
                        st.session_state.workflow_step = 8
                        st.success("✅ Dual-Agent Orchestration Complete!")
                        st.experimental_rerun()
                        
                    except json.JSONDecodeError:
                        st.error("Error parsing judge decision")
                        
                except Exception as e:
                    st.error(f"Error in orchestration: {str(e)}")
        else:
            st.error("Please enter clinical notes before starting orchestration")

# Orchestration results are displayed in the Live Agent Conversations section below

# Workflow Insights & Supporting Data
if st.session_state.workflow_step >= 3:
    st.markdown("---")
    st.header("📊 Live Agent Conversations & Data Sources")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💬 Agent Chat History")
        
        # Show actual agent conversations
        if st.session_state.generated_claim:
            with st.expander("🤖 Builder Agent Response", expanded=True):
                st.markdown("**Input:** Patient data + Clinical notes + Procedure info")
                st.code(st.session_state.generated_claim, language='json')
        
        if st.session_state.insurance_rebuttal:
            with st.expander("🛡️ Insurance Agent Response", expanded=True):
                st.markdown("**Input:** Generated claim + Policy documents")
                st.code(st.session_state.insurance_rebuttal, language='json')
                
        if st.session_state.judge_decision:
            with st.expander("⚖️ AI Judge Decision", expanded=True):
                st.markdown("**Input:** Both agent outputs + Context")
                st.code(st.session_state.judge_decision, language='json')
        
        # Appeals Conversation History (moved here from appeals section)
        if st.session_state.appeal_history:
            st.subheader("💬 Appeals Conversation History")
            for appeal in st.session_state.appeal_history:
                if appeal['type'] == 'DOCTOR_APPEAL':
                    with st.expander(f"📋 Doctor Appeal - Round {appeal['round']}", expanded=True):
                        st.markdown("**Input:** Original claim + Insurance analysis + Judge decision")
                        try:
                            appeal_json = json.loads(appeal['content'])
                            st.markdown(f"**Appeal Summary:** {appeal_json.get('appeal_summary', 'N/A')}")
                            st.markdown(f"**Medical Justification:** {appeal_json.get('medical_justification', 'N/A')}")
                            evidence = appeal_json.get('additional_evidence', [])
                            if evidence:
                                st.markdown("**Additional Evidence:**")
                                for item in evidence:
                                    st.markdown(f"• {item}")
                            st.code(appeal['content'], language='json')
                        except:
                            st.text(appeal['content'])
                            
                elif appeal['type'] == 'INSURANCE_COUNTER':
                    with st.expander(f"🛡️ Insurance Counter-Appeal - Round {appeal['round']}", expanded=True):
                        st.markdown("**Input:** Doctor appeal + Original analysis")
                        try:
                            counter_json = json.loads(appeal['content'])
                            st.markdown(f"**Counter Response:** {counter_json.get('counter_response', 'N/A')}")
                            st.markdown(f"**Position:** {counter_json.get('position_change', 'N/A')}")
                            st.markdown(f"**New Strength Score:** {counter_json.get('new_strength_score', 'N/A')}")
                            st.markdown(f"**Final Recommendation:** {counter_json.get('final_recommendation', 'N/A')}")
                            st.code(appeal['content'], language='json')
                        except:
                            st.text(appeal['content'])
    
    with col2:
        st.subheader("📊 Live Data Sources")
        
        # Show actual policy documents being used
        with st.expander("📖 Active Policy Documents"):
            try:
                policy_query = "SELECT DOCUMENT_TYPE, DOCUMENT_CONTENT FROM CLAIMS_DEMO.PUBLIC.CIGNA_POLICY_DOCUMENTS LIMIT 1"
                policy_result = session.sql(policy_query).collect()
                if policy_result:
                    policy_doc = policy_result[0]['DOCUMENT_CONTENT']
                    st.text_area("Sample Policy Content:", policy_doc[:500] + "...", height=150)
                    st.caption("Policy documents are searched dynamically during insurance analysis")
            except:
                st.error("Could not load policy documents")
        
        # Show patient data being used
        if 'selected_patient' in locals() and selected_patient:
            patient_id = selected_patient.split(' - ')[0]
            with st.expander("👤 Patient Data in Use"):
                try:
                    patient_query = f"SELECT * FROM CLAIMS_DEMO.PUBLIC.PATIENTS WHERE PATIENT_ID = '{patient_id}'"
                    patient_result = session.sql(patient_query).collect()
                    if patient_result:
                        patient_data = dict(patient_result[0])
                        for key, value in patient_data.items():
                            st.write(f"**{key}:** {value}")
                    else:
                        st.write("No patient data found")
                except Exception as e:
                    st.error(f"Could not load patient data: {str(e)}")
        
        # Show procedure data being used
        if 'selected_procedure' in locals() and selected_procedure:
            procedure_code = selected_procedure.split(' - ')[0]
            with st.expander("🏥 Procedure Data in Use"):
                try:
                    proc_query = f"SELECT * FROM CLAIMS_DEMO.PUBLIC.COMMON_PROCEDURES WHERE PROCEDURE_CODE = '{procedure_code}'"
                    proc_result = session.sql(proc_query).collect()
                    if proc_result:
                        proc_data = dict(proc_result[0])
                        for key, value in proc_data.items():
                            st.write(f"**{key}:** {value}")
                    else:
                        st.write("No procedure data found")
                except Exception as e:
                    st.error(f"Could not load procedure data: {str(e)}")
    
    # Show dynamic scoring analysis
    if st.session_state.insurance_rebuttal:
        st.subheader("🔍 Scoring Analysis")
        try:
            rebuttal_json = json.loads(st.session_state.insurance_rebuttal)
            strength_score = rebuttal_json.get('strength_score', 0)
            
            # Check why score might be low
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Claim Strength", f"{strength_score:.2f}/1.0")
            with col2:
                denial_count = len(rebuttal_json.get('denial_reasons', []))
                st.metric("Issues Found", denial_count)
            with col3:
                policy_count = len(rebuttal_json.get('policy_citations', []))
                st.metric("Policy Citations", policy_count)
                
            # Show what's affecting the score
            st.write("**Factors affecting score:**")
            for reason in rebuttal_json.get('denial_reasons', []):
                st.write(f"❌ {reason}")
                
        except json.JSONDecodeError:
            st.error("Could not parse insurance analysis")

# Reset workflow button (moved to bottom)
if st.session_state.workflow_step > 1:
    st.markdown("---")
    if st.button("🔄 Reset Workflow", use_container_width=True):
        st.session_state.workflow_step = 1
        st.session_state.generated_claim = None
        st.session_state.insurance_rebuttal = None
        st.session_state.judge_decision = None
        st.session_state.appeals_round = 0
        st.session_state.final_decision = None
        st.session_state.appeal_history = []
        st.experimental_rerun()
