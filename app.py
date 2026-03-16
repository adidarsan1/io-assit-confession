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

Format your response EXACTLY like this with these exact sections:

--- DRAFT ---
(Header: சம்பவ இட ஆய்வு மகஜர் / ஒப்புதல் வாக்குமூலம்)
(Body: Professional Legal Prose)
(Signature Clause: "சாட்சிகளுக்கு வாசித்துக் காட்டப்பட்டு சம்மதம் பெறப்பட்டது.")

--- DEFENSE_RISK_ANALYSIS ---
Provide a bulleted list of missing details from the IO's input that the defense lawyer could exploit in court. Examples:
- "Light source not mentioned. Defense will claim it was too dark to see."
- "Witnesses names not provided. Need 2 independent witnesses."
- "Time of arrest/seizure missing."
(Translate this analysis conceptually into clear English for the IO).
"""

# 3. Streamlit UI (The "Anti-Gravity" Theme)
st.set_page_config(
    page_title="Anti-Gravity IO Assist", 
    page_icon="👮", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

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
st.markdown("### 📝 Enter Raw Notes (Tanglish/Local)")
st.info("💡 Pro-Tip: Use your mobile keyboard's microphone 🎙️ for fast Tamil voice typing.")

raw_input = st.text_area("Example: Accused knife-ah bridge pakkam ditch-la hidden panni vachiruken nu sonnan. 2 witnesses irukanga.", height=200)

if st.button("🚀 GENERATE LEGAL DRAFT", type="primary"):
    if not raw_input:
        st.error("Please enter some notes!")
        else:
            with st.spinner("Processing with Anti-Gravity Intelligence..."):
                import requests
                
                # Direct REST call matching exactly with io-assist-anti-gravity reference
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={GOOGLE_API_KEY}"
                
                user_msg = f"Document Type: {doc_type}\nCase Info: {fir_details}, {station}\nInput: {raw_input}"
                
                payload = {
                    "system_instruction": {"parts": [{"text": SYSTEM_PROMPT}]},
                    "contents": [{"parts": [{"text": user_msg}]}],
                    "generationConfig": {
                        "temperature": 0.2,
                        "maxOutputTokens": 8192,
                        "candidateCount": 1
                    }
                }
                
                try:
                    resp = requests.post(url, json=payload, timeout=90)
                    if resp.status_code == 200:
                        data = resp.json()
                        candidates = data.get("candidates", [])
                        if candidates:
                            raw_resp = candidates[0]["content"]["parts"][0]["text"]
                            draft_part = raw_resp
                            risk_part = ""
                            
                            # Parse out the two sections we defined in the prompt
                            if "--- DEFENSE_RISK_ANALYSIS ---" in raw_resp:
                                parts = raw_resp.split("--- DEFENSE_RISK_ANALYSIS ---")
                                draft_part = parts[0].replace("--- DRAFT ---", "").strip()
                                risk_part = parts[1].strip()
                            else:
                                draft_part = raw_resp.replace("--- DRAFT ---", "").strip()
                                
                            st.session_state.output = draft_part
                            st.session_state.defense_risks = risk_part
                        else:
                            st.error("🚨 Error: Empty response from Gemini. Try adding more notes.")
                    elif resp.status_code == 400:
                        st.error("🚨 API Key Error: Invalid API key. Please check your Secrets configuration.")
                    elif resp.status_code == 429:
                        st.error("🚨 Quota Error: Rate limit hit. Wait 1 minute and try again.")
                    elif resp.status_code == 404:
                        st.error(f"🚨 Model Error (404): Model not found. API Response: {resp.text[:200]}")
                    else:
                        st.error(f"🚨 API Error ({resp.status_code}): {resp.text[:300]}")
                except requests.exceptions.Timeout:
                    st.error("🚨 Timeout: Server took too long. Check your internet and try again.")
                except Exception as e:
                    st.error(f"🚨 Connection Error: {str(e)}")

st.markdown("---")
st.markdown("### 📜 CCTNS Ready Draft")
if 'output' in st.session_state:
    st.markdown("<p style='color: #a0a0a0; font-size: 0.9rem; margin-bottom: 5px;'>Use the copy icon on the top right of the box below to copy to CCTNS.</p>", unsafe_allow_html=True)
    st.code(st.session_state.output, language="markdown")
    
    # Display Defense Risk Analysis below the draft in a visual warning box
    if st.session_state.get('defense_risks'):
        st.markdown("### 🛡️ Defense Risk Analysis")
        st.warning(st.session_state.defense_risks)
        
    st.success("Defense-Proofing Clauses Added Successfully!")
else:
    st.info("The formal draft will appear here.")

st.divider()
st.caption("Anti-Gravity IO Tool v2.0 | Designed for Tamil Nadu Police | Procedural Law Compliant")
