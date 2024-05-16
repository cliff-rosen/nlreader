import google.oauth2.credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import os, pickle
import base64
from flask import session, redirect, url_for

# If modifying these scopes, delete the file token.pickle.
SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/gmail.readonly",
]
# CREDENTIALS_FILE = "C:\\code\\nlreader\\backend\\src\\secrets\\client_secret_604005571-hu893qnfe3nns3rj4uvc4a0clgji88da.apps.googleusercontent.com.json"
CLIENT_SECRETS_FILE = "C:\\code\\nlreader\\backend\\src\\secrets\\client_secret_604005571-miie2779t7p81l65up26sb6dih1q7uoe.apps.googleusercontent.com.json"
REDIRECT_URI = "http://localhost:3000/auth_callback"


def test():
    creds = {}
    service = build("gmail", "v1", credentials=creds)
    return service


def credentials_to_dict(credentials):
    return {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
    }


def credentials_from_dict(creds_dict):
    credentials = google.oauth2.credentials.Credentials(**creds_dict)
    return credentials


def get_service_from_creds(creds):
    service = build("gmail", "v1", credentials=creds)
    return service


def get_auth_url():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES)
    # flow.redirect_uri = url_for("google_auth_callback", _external=True)
    flow.redirect_uri = REDIRECT_URI
    authorization_url, state = flow.authorization_url(
        access_type="offline", include_granted_scopes="true"
    )
    # session["oauth_state"] = state
    print("---------------------------------")
    print(authorization_url)
    return authorization_url


def get_token_from_auth_code(auth_code):
    print("get_token_from_auth_code")
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES)
    flow.redirect_uri = REDIRECT_URI

    try:
        token_response = flow.fetch_token(code=auth_code)
        credentials = flow.credentials
        credentials_dict = credentials_to_dict(credentials)
        # with open("secrets/token.pickle", "wb") as token:
        #     pickle.dump(credentials, token)
    except Exception as e:
        raise Exception(f"Failed to fetch access token: {e}")

    # return token_response
    return credentials_dict


### Google API wrappers ###


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


def get_labels(service):
    labels = service.users().labels().list(userId="me").execute().get("labels", [])

    return labels


##########################################


def get_service_old():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("secrets/token.pickle"):
        with open("secrets/token.pickle", "rb") as token:
            creds = pickle.load(token)
        print(vars(creds))
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("secrets/token.pickle", "wb") as token:
            pickle.dump(creds, token)

    service = build("gmail", "v1", credentials=creds)
    return service
