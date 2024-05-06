from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import os, pickle
import base64
from flask import session, redirect, url_for

# If modifying these scopes, delete the file token.pickle.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly", "openid"]
CREDENTIALS_FILE = "C:\\code\\nlreader\\backend\\src\\secrets\\client_secret_604005571-hu893qnfe3nns3rj4uvc4a0clgji88da.apps.googleusercontent.com.json"


def get_auth_url():
    flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, scopes=SCOPES)
    # flow.redirect_uri = url_for("google_auth_callback", _external=True)
    flow.redirect_uri = "https://localhost/get_token_from_auth_code"
    authorization_url, state = flow.authorization_url(
        access_type="offline", include_granted_scopes="true"
    )
    # session["oauth_state"] = state
    print("---------------------------------")
    print(authorization_url)
    return authorization_url


def get_token_from_auth_code(auth_code):
    return 0


def get_service():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("secrets/token.pickle"):
        with open("secrets/token.pickle", "rb") as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("secrets/token.pickle", "wb") as token:
            pickle.dump(creds, token)

    service = build("gmail", "v1", credentials=creds)
    return service


def get_messages(service, label, start_date, end_date):
    query = f"after:{start_date} before:{end_date}"
    results = (
        service.users()
        .messages()
        .list(userId="me", labelIds=[label], maxResults=100, q=query)
        .execute()
    )
    return results.get("messages", [])


def get_message(service, id):
    msg = (
        service.users()
        .messages()
        .get(
            userId="me",
            id=id,
            metadataHeaders=["Subject"],
        )
        .execute()
    )
    payload = msg.get("payload", {})
    headers = payload.get("headers", [])
    subject = next(
        (header["value"] for header in headers if header["name"] == "Subject"),
        "No Subject",
    )
    text = get_message_text(msg)
    return {"msg": msg, "subject": subject, "text": text}


def get_message_text(message):
    payload = message.get("payload", {})
    parts = payload.get("parts", [])
    text = ""
    for part in parts:
        data = part["body"]["data"]
        data_decoded = base64.urlsafe_b64decode(data.encode("ASCII")).decode("utf-8")
        # print(part["mimeType"])
        # print(data_decoded[:100])
        if part["mimeType"] == "text/plain":
            text += data_decoded
    return text


def get_labels():
    service = get_service()
    labels = service.users().labels().list(userId="me").execute().get("labels", [])

    return labels
