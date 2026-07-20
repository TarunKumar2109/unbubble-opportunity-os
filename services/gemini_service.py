import json
import os

import streamlit as st
st.error("RUNNING GEMINI_SERVICE VERSION 8a528ce")
from dotenv import load_dotenv
from google import genai

# -------------------------------------------------
# Load Environment Variables
# -------------------------------------------------

load_dotenv()

API_KEY = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found.")

# -------------------------------------------------
# Gemini Client
# -------------------------------------------------

MODELS = [
    "gemini-3.5-flash",
    "gemini-flash-latest",
    "gemini-pro-latest",
    "gemini-2.5-flash"
]

client = genai.Client(api_key=API_KEY)

# -------------------------------------------------
# Prompt
# -------------------------------------------------

SYSTEM_PROMPT = """
You are an Opportunity Intelligence Engine.

Extract the opportunity information from the given text.

Return ONLY valid JSON.

Do not use markdown.
Do not wrap the JSON inside ```.

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

    last_error = None

    for model in MODELS:

        try:

            response = client.models.generate_content(
                model=model,
                contents=[
                    SYSTEM_PROMPT,
                    text
                ]
            )

            output = response.text.strip()

            return json.loads(output)

        except json.JSONDecodeError:

            return {
                "error": True,
                "raw_response": output
            }

        except Exception as e:

            last_error = e
            continue

    st.exception(last_error)

    return {
        "error": True,
        "raw_response": str(last_error)
    }