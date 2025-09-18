import streamlit as st
from google.cloud import dialogflow_v2 as dialogflow
from google.oauth2 import service_account

st.title("🩺 HealthBot - Dialogflow AI Chatbot")

# 🔑 Hardcoded Service Account JSON
creds_info = {
  "type": "service_account",
  "project_id": "healthbot-472404",
  "private_key_id": "1fbef5726917df2243925eed21b9c562ff593e67",
  "private_key": """-----BEGIN PRIVATE KEY-----
MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQC7pLiovTpm/TNS
EFG+M05B8cnhA/IFNdjFWzoO29yBoTo7gC7utQXwzTxt+luWh5efgVQRDPxgppPB
BeWmX7OCDXrCt+mzpiakX6kjC711ZfqwPVcBjGrhDDI13u5KLjrBICDpLUnveRXb
HgSrQim0DS83AgFQGVbFUs4+7EIwWr/w7ORYKh0G2ObRdntDNTaxP/+Qz1zoAt+I
FSok1ZvzfrBoliO8uGBG0TupTStUfeW+5qzEwBUuhAiV+LzG5gNzuqSCKBSCLaUm
vs484hr1f/0138VdUbrTv4nDVczqprdOWcsvrcb8yNC+tlQNPadO0Zq0wdbdSyne
MxmpjtKLAgMBAAECggEAFHnXmrY3esiTgpd8TAyONBz94huLm+zx0CtxzPBKAi1F
TPviYzMGyG2k8/1XZDg8n++9bDTmD2fuBKivlDWqQX1WEYx/KJbvbY1wx/2+eWKc
9gFjjqwzd4Zcrks65oZf6/YlETzbbhHhBC2k5clNArRTnCWQXhy9vr+X+P7QBDWb
FU0FnnyxFpdJs4MIAaMVBPLHpl73pgEp2TFjjVU/Z/o8RPthg1IfgUKcl9k5Y6bK
H3uQeNVOKidvS8NM6C37Q71/ZNIK3r9ghRkKoFKbAqt9++QlDNAznWuc9t4+TBEy
/9afrUp4By4Iw/mb1GSqGh/kvKTXi7BAI4rOb20suQKBgQDhS7dbWzPRwRkptDIA
Tnevu9vewoOAAtYsfdccOuCa/zsmQ+rs1fVaG2fi+TnvRDkN8SIbVrwU89WS6l5q
+yItzEdXAqt9FQTP2y1JdfLnZYW4647XfgcKbFz8QQHBHPGKqvQ3owgklvWLLQWc
WCLaK4g420i/2yVm5c5mqzkYiQKBgQDVN1z8ZXWaLRbpPaxO1KCmzHJoUn1C+HCg
/FhEQ2JjzHPtivhpAnIYEnUA5dkp9HLQYlXVKSaZNTN2ynTDQRe1TcnIYGrdhhnX
uvKXXEUVaWgV4lJ4depKij4m07RjEJN4Kv1/OE4HSQ93QSuPmOEUTyfYfww5sbzP
2LuvmjUlcwKBgGlbt0uJwxn8a4ANPLTX/TC5cYEjBcv/h5kW4FnbTt4tLcQfTuWi
yTJyTorecjFqfiP++CxAy4Qg42fpIm51Mu6n8VTHctrz0WRC41LPTeDYoUhxIEO2
NCSzuGhfHirpFiv69mpuW4iA8CM90rninanZYcL1CXhvS3ZrUbLBr9nBAoGAOeCj
bygjekyPEZVaNrPlQCHzVHo/4nQKLskRNMaN6MVRGsRElkzBp+Mqu6mo/4iJuiNX
ZVucTK5yX+apN29t/hs1kR0LJUMHtNXckFXNsvg/9uDOvkBT7xQDtwp0xwdy4IXa
9jPUiom8lwSrzHkVcCvkhxJFwUuME2ej2xEjKB0CgYBXGjkLzjieTYm2RpTc17AU
zi3hB+DVTHYmo9wXd38qQxbW+Lmj1Y+2DKmbRO1y9NbXuEAtmiPGOFRcYbQpVdcj
cTihumMQM3iQR2GKzzwhy7YuFeKCihkrRc9XRcIcAo6mko6DqpDkN1/3+idUzO1J
Qdpz2ST/hdxGRSfCy78MaA==
-----END PRIVATE KEY-----\n""",
  "client_email": "dialogflow-sa@healthbot-472404.iam.gserviceaccount.com",
  "client_id": "117001537007152603347",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/dialogflow-sa%40healthbot-472404.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

# ✅ Build credentials directly
credentials = service_account.Credentials.from_service_account_info(creds_info)
PROJECT_ID = creds_info["project_id"]

# ✅ Dialogflow Client
session_client = dialogflow.SessionsClient(credentials=credentials)

def detect_intent_text(text, session_id="streamlit-session", language_code="en"):
    session = session_client.session_path(PROJECT_ID, session_id)
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    return response.query_result.fulfillment_text

# 🖥️ Streamlit UI
user_input = st.text_input("💬 Type your health query:")
if user_input:
    try:
        response = detect_intent_text(user_input)
        st.write("🤖 Bot:", response)
    except Exception as e:
        st.error(f"⚠️ Error while talking to Dialogflow: {e}")
