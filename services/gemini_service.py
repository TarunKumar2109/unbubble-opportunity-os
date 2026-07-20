import json
import os

from dotenv import load_dotenv
from google import genai

# -----------------------------------------
# Load Environment Variables
# -----------------------------------------

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file.")

# -----------------------------------------
# Gemini Client
# -----------------------------------------

MODEL_NAME = "gemini-3.5-flash"

client = genai.Client(api_key=API_KEY)

# -----------------------------------------
# Prompt
# -----------------------------------------

SYSTEM_PROMPT = """
You are an Opportunity Intelligence Engine.

Extract the opportunity information from the provided text.

Return ONLY valid JSON.

Do not use markdown.
Do not wrap the JSON in ```.

Use this exact schema:

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

# -----------------------------------------
# Extract Opportunity
# -----------------------------------------

def extract_opportunity(text: str):

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