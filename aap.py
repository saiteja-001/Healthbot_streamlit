# app.py
import os
from flask import Flask, request, jsonify
from twilio.rest import Client
from google.cloud import dialogflow_v2 as dialogflow
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Env variables (make sure you set them in your .env)
PROJECT_ID = os.environ.get("DIALOGFLOW_PROJECT_ID")
GOOGLE_CREDS = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.environ.get("TWILIO_WHATSAPP_NUMBER")  # e.g. 'whatsapp:+1415XXXXXXX'

# Ensure creds are loaded
if not PROJECT_ID or not GOOGLE_CREDS:
    raise Exception("Missing Dialogflow credentials. Check DIALOGFLOW_PROJECT_ID and GOOGLE_APPLICATION_CREDENTIALS.")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_CREDS

# Flask app
app = Flask(__name__)
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Function to call Dialogflow
def detect_intent_text(text, session_id="default-session", language_code="en"):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(PROJECT_ID, session_id)
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    return response.query_result.fulfillment_text, response.query_result.intent.display_name

# API endpoint for web/Streamlit testing
@app.route("/message", methods=["POST"])
def message():
    data = request.get_json(force=True)
    text = data.get("text", "")
    session_id = data.get("session_id", "web-session")
    language = data.get("language", "en")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    reply, intent = detect_intent_text(text, session_id=session_id, language_code=language)
    return jsonify({"reply": reply, "intent": intent})

# Twilio webhook endpoint (WhatsApp/SMS)
@app.route("/twilio", methods=["POST"])
def twilio_webhook():
    from_number = request.form.get("From")  # e.g. whatsapp:+91XXXXXXXXXX
    body = request.form.get("Body") or ""

    session_id = from_number.replace(":", "_") if from_number else "twilio-session"
    language = "en"  # You can switch to 'hi' for Hindi

    try:
        reply_text, intent = detect_intent_text(body, session_id=session_id, language_code=language)
    except Exception as e:
        print("Dialogflow error:", e)
        reply_text = "Sorry, something went wrong."

    # Send reply back to WhatsApp
    try:
        twilio_client.messages.create(
            body=reply_text,
            from_=TWILIO_WHATSAPP_NUMBER,
            to=from_number
        )
        print(f"Replied to {from_number} with: {reply_text}")
    except Exception as e:
        print("Twilio send error:", e)

    return ("", 200)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
