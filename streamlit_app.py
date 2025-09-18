import os
import json
import streamlit as st
from google.cloud import dialogflow_v2 as dialogflow

# Load service account from Streamlit Secrets
creds = st.secrets["google_service_account"]

# Write creds to a temporary JSON file
with open("service_account.json", "w") as f:
    json.dump(dict(creds), f)

# Point Google auth to this file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service_account.json"

PROJECT_ID = creds["project_id"]

def detect_intent_text(text, session_id="streamlit-session", language_code="en"):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(PROJECT_ID, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    return response.query_result.fulfillment_text

st.title("💬 HealthBot")

user_input = st.text_input("You:", "")

if st.button("Send") and user_input:
    response_text = detect_intent_text(user_input)
    st.write("🤖 Bot:", response_text)
