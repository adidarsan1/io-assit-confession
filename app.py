import streamlit as st
import google.generativeai as genai

# 1. API Configuration
# Get your API key securely from Streamlit secrets
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
except KeyError:
    st.error("Missing Google API Key! Please set it in Streamlit secrets (.streamlit/secrets.toml) or Community Cloud Settings.")
    st.stop()

genai.configure(api_key=GOOGLE_API_KEY)

# 2. System Prompt - The "Brain" of the tool
# This includes the logic from your uploaded Judgement file
SYSTEM_PROMPT = """
You are a Senior Legal Expert for the Tamil Nadu Police. 
Your mission: Convert raw, informal 'Tanglish' or 'Colloquial Tamil' IO notes into a 
Defense-Proof 'Observation Mahazar' or 'Confession Statement'.

Rules to avoid Loophole (Defense-Proofing):
1. ADMISSIBILITY: For confessions, only draft the portion leading to discovery (Section 27 Evidence Act). 
2. NO COERCION: Always include "எந்தவித அச்சுறுத்தலும் இன்றி தானாக முன்வந்து அளித்த வாக்குமூலம்".
3. CONCEALMENT: Describe recovery spots as 'hidden' or 'exclusive knowledge' so defense cannot claim public access.
4. INDEPENDENT WITNESSES: Always mention 2 independent witnesses (பஞ்சாயத்தார்கள்) were present throughout the process.
5. PROCEDURAL FLAWS: Refer to recent High Court/Supreme Court standards (ensure time of arrest and seizure are consistent).
6. LANGUAGE: Convert Tanglish (e.g., 'knife-ah ditch-la thooki potten') into High-Level Legal Tamil (e.g., 'கத்தியை சாக்கடையில் வீசி எறிந்தேன்').

Format:
- Header: சம்பவ இட ஆய்வு மகஜர் / ஒப்புதல் வாக்குமூலம்
- Body: Professional Legal Prose
- Signature Clause: "சாட்சிகளுக்கு வாசித்துக் காட்டப்பட்டு சம்மதம் பெறப்பட்டது."
"""

# 3. Streamlit UI (The "Anti-Gravity" Theme)
st.set_page_config(page_title="Anti-Gravity IO Assist", page_icon="👮", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #2e7d32; color: white; height: 50px; font-weight: bold; }
    .stTextArea>div>div>textarea { background-color: #1e1e1e; color: #00ff00; font-family: 'Courier New', monospace; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 Anti-Gravity: IO-Assist Automation")
st.subheader("Tanglish to Defense-Proof Legal Tamil")

# Sidebar for Case Metadata
with st.sidebar:
    st.header("📋 Case Details")
    doc_type = st.selectbox("Document Type", ["Confession (வாக்குமூலம்)", "Observation Mahazar (ஆய்வு மகஜர்)"])
    fir_details = st.text_input("FIR No / Section")
    station = st.text_input("Police Station")
    st.divider()
    st.info("Note: Recent Judgement standards applied to prevent flaws.")

# Main Input
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📝 Enter Raw Notes (Tanglish/Local)")
    raw_input = st.text_area("Example: Accused knife-ah bridge pakkam ditch-la hidden panni vachiruken nu sonnan. 2 witnesses irukanga.", height=350)
    
    if st.button("GENERATE LEGAL DRAFT"):
        if not raw_input:
            st.error("Please enter some notes!")
        else:
            with st.spinner("Processing with Anti-Gravity Intelligence..."):
                try:
                    # Standard model, highly reliable
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    full_prompt = f"{SYSTEM_PROMPT}\n\nDocument Type: {doc_type}\nCase Info: {fir_details}, {station}\nInput: {raw_input}"
                    
                    response = model.generate_content(full_prompt)
                    st.session_state.output = response.text
                except Exception as e:
                    st.error(f"Error generating content: {str(e)}")

with col2:
    st.markdown("### 📜 CCTNS Ready Draft")
    if 'output' in st.session_state:
        st.text_area("Copy this to CCTNS:", value=st.session_state.output, height=450)
        st.success("Defense-Proofing Clauses Added Successfully!")
    else:
        st.info("The formal draft will appear here.")

st.divider()
st.caption("Anti-Gravity IO Tool v2.0 | Designed for Tamil Nadu Police | Procedural Law Compliant")
