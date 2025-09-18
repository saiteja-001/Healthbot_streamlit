import os
import streamlit as st
from google.cloud import dialogflow_v2 as dialogflow

# ✅ Point to your service account JSON (must be in repo root)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "healthbot-472404-1fbef5726917.json"

# ✅ Your Dialogflow Project ID
PROJECT_ID = "healthbot-472404"   # replace if your actual ID is different

# 🔎 Function to query Dialogflow
def detect_intent_text(text, session_id="streamlit-session", language_code="en"):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(PROJECT_ID, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    return response.query_result.fulfillment_text

# 🎨 Streamlit UI
st.title("🩺 AI HealthBot")
st.write("Ask me about **symptoms, prevention, or vaccination schedules** (English/Hindi).")

# Store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])

# User input
if prompt := st.chat_input("Type your health query..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)

    try:
        reply = detect_intent_text(prompt)
    except Exception as e:
        reply = f"⚠️ Error: {str(e)}"

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").markdown(reply)

