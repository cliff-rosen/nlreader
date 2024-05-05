# server.py
from flask import url_for
from google_auth_oauthlib.flow import Flow
import google.oauth2.credentials
import google_auth_oauthlib.flow
import os


# Google OAuth 2.0 credentials
CLIENT_SECRETS_FILE = "secrets\client_secret_604005571-hu893qnfe3nns3rj4uvc4a0clgji88da.apps.googleusercontent.com.json"
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def login():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES
    )
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


print(login())
