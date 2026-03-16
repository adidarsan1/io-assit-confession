# Anti-Gravity: IO-Assist Automation

A Streamlit web application designed for the Tamil Nadu Police to convert raw, informal 'Tanglish' or 'Colloquial Tamil' IO notes into Defense-Proof 'Observation Mahazars' or 'Confession Statements' using the Gemini Pro AI model.

## Features
- Generates Defense-Proof legal documents (Confession Statements / Observation Mahazar).
- Automatically formats output into Professional Legal Tamil.
- Ensures admissibility according to Section 27 of Evidence Act.

## How to run locally
1. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
2. Create `.streamlit/secrets.toml` with your Gemini API key:
   ```toml
   GOOGLE_API_KEY = "your-api-key"
   ```
3. Run the application:
   ```bash
   streamlit run app.py
   ```
