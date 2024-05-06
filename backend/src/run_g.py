# server.py
from flask import url_for
from google_auth_oauthlib.flow import InstalledAppFlow
import google.oauth2.credentials
import os


# Google OAuth 2.0 credentials
CREDENTIALS_FILE = "C:\\code\\nlreader\\backend\\src\\secrets\\client_secret_604005571-hu893qnfe3nns3rj4uvc4a0clgji88da.apps.googleusercontent.com.json"
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def login():
    flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, scopes=SCOPES)
    # flow.redirect_uri = url_for("google_auth_callback", _external=True)
    flow.redirect_uri = "https://localhost"
    authorization_url, state = flow.authorization_url(
        access_type="offline", include_granted_scopes="true"
    )
    print("state:", state)
    return authorization_url


def google_auth_callback():
    state = session["oauth_state"]
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, state=state
    )
    flow.redirect_uri = url_for("google_auth_callback", _external=True)
    flow.fetch_token(authorization_response=request.url)
    credentials = flow.credentials
    session["credentials"] = credentials_to_dict(credentials)
    return redirect("/")


def credentials_to_dict(credentials):
    return {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
    }


 flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, scopes=SCOPES)
flow.redirect_uri = "http://localhost"
authorization_code = (
    "4/0AdLIrYceZslN4Rupt-sv9r6ivFFWH4C4w7woc8zHQ00uKZOz083OrasD49_gZF8mgQ5woA"
)
creds = flow.fetch_token(code=authorization_code)
print(creds)
