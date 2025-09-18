import os
import json
import streamlit as st
from google.cloud import dialogflow_v2 as dialogflow

st.set_page_config(page_title="HealthBot", page_icon="💬")

# -----------------------------
# Load service account from Streamlit Secrets
# -----------------------------
creds = st.secrets["google_service_account"]

# Write creds into a temporary JSON file
with open("service_account.json", "w") as f:
    json.dump(dict(creds), f)

# Point Google auth to this file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service_account.json"

# Fixed Project ID (from your service account JSON)
PROJECT_ID = "healthbot-472404"

# -----------------------------
# Function to call Dialogflow
# -----------------------------
def detect_intent_text(text, session_id="streamlit-session", language_code="en"):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(PROJECT_ID, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    return response.query_result.fulfillment_text

# -----------------------------
# Streamlit UI
# -----------------------------
st.title("💬 HealthBot - AI Health Assistant")

st.write("Ask me anything about preventive healthcare, symptoms, or vaccinations!")

user_input = st.text_input("You:", "")

if st.button("Send") and user_input.strip():
    try:
        response_text = detect_intent_text(user_input)
        st.success(f"🤖 Bot: {response_text}")
    except Exception as e:
        st.error(f"⚠️ Error: {str(e)}")
