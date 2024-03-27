from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import os, pickle

# If modifying these scopes, delete the file token.pickle.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
CREDENTIALS_FILE = "secrets/client_secret_604005571-hu893qnfe3nns3rj4uvc4a0clgji88da.apps.googleusercontent.com.json"


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
            format="metadata",
            metadataHeaders=["Subject"],
        )
        .execute()
    )
    return msg


def get_labels():
    service = get_service()
    labels = service.users().labels().list(userId="me").execute().get("labels", [])

    return labels
