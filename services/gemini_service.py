import json
import os

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import errors

# -------------------------------------------------
# Load Environment Variables
# -------------------------------------------------

load_dotenv()

API_KEY = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

st.write("✅ API Loaded:", API_KEY is not None)

if API_KEY:
    st.write("🔑 Key Prefix:", API_KEY[:6])

if not API_KEY:
    raise ValueError("❌ GEMINI_API_KEY not found.")

# -------------------------------------------------
# Gemini Client
# -------------------------------------------------

MODEL_NAME = "gemini-2.5-flash-lite"

client = genai.Client(api_key=API_KEY)

# -------------------------------------------------
# Prompt
# -------------------------------------------------

SYSTEM_PROMPT = """
You are an Opportunity Intelligence Engine.

Extract opportunity information from the given text.

Return ONLY valid JSON.

Do NOT use markdown.
Do NOT wrap the JSON inside ```.

Use exactly this schema:

{
"title":"",
"organizer":"",
"category":"",
"deadline":"",
"website":"",
"funding_amount":"",
"eligibility":"",
"location":"",
"summary":"",
"description":"",
"required_documents":[],
"contact_email":"",
"application_process":"",
"relevance_score":0,
"reason_for_score":"",
"recommended_action":"",
"confidence":0
}
"""

# -------------------------------------------------
# Extract Opportunity
# -------------------------------------------------

def extract_opportunity(text: str):

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=[
                SYSTEM_PROMPT,
                text
            ]
        )

        output = response.text.strip()

        try:
            return json.loads(output)

        except json.JSONDecodeError:
            return {
                "error": True,
                "raw_response": output
            }

    except Exception as e:
        st.exception(e)
        raise