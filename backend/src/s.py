# server.py
from flask import Flask, jsonify, redirect, request, session, url_for
from google_auth_oauthlib.flow import Flow
import google.oauth2.credentials
import google_auth_oauthlib.flow
import os

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "super_secret_key")

# Google OAuth 2.0 credentials
CLIENT_SECRETS_FILE = "path_to_your_client_secret_json_file.json"
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


@app.route("/login")
def login():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES
    )
    flow.redirect_uri = url_for("google_auth_callback", _external=True)
    authorization_url, state = flow.authorization_url(
        access_type="offline", include_granted_scopes="true"
    )
    session["oauth_state"] = state
    return redirect(authorization_url)


@app.route("/auth/google/callback")
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


@app.route("/logout")
def logout():
    session.pop("credentials", None)
    return redirect("/")


@app.route("/api/messages")
def get_messages():
    if "credentials" not in session:
        return redirect("/login")

    credentials = google.oauth2.credentials.Credentials(**session["credentials"])

    # Use the credentials to access Gmail API and fetch messages
    # (similar to the previous code)
    ...


def credentials_to_dict(credentials):
    return {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
    }


if __name__ == "__main__":
    app.run(debug=True)
