# server.py
from flask import url_for
from google_auth_oauthlib.flow import InstalledAppFlow
import google.oauth2.credentials
import os


# Google OAuth 2.0 credentials
CREDENTIALS_FILE = "C:\\code\\nlreader\\backend\\src\\secrets\\client_secret_604005571-miie2779t7p81l65up26sb6dih1q7uoe.apps.googleusercontent.com.json"
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
]
SCOPES = "https://www.googleapis.com/auth/gmail.readonly openid https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email"


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
flow.redirect_uri = "http://localhost:3000"
authorization_code = (
    "4/0AdLIrYf0ZpSQhbYSYlUhaMvFz2YTZ1nLPKJFoLlCvPZ5f3n-HPrXEIxVi8CNTfCW5qQe6Q"
)
creds = flow.fetch_token(code=authorization_code)
print(creds)

{
    "access_token": "ya29.a0AXooCgv-m6QJKHkTR1f3n1DjMKpUoHSs2RFNy4ueHcv3dAoU_Pt414tiQLt0MewqPdzCa3hyq8XW1yfGJxc5XMcbANt0fuXurQyD4XPFkCxb5XwcV9nWM22kGozy9sOsY1qeJB5L30qFbOSwFBieo6BnH_m7cIBdvZHbaCgYKASMSARASFQHGX2MiKJOxeU25HKaH_RksIXvv_g0171",
    "expires_in": 3599,
    "refresh_token": "1//04cymfDXfcJ00CgYIARAAGAQSNgF-L9Ir4j4AGjE3zV2E0DPK2fga1tsjYARRAOyJ0f1l3k_Hzk-0B51qeJ76BKSMoflkDy5ZhQ",
    "scope": [
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/userinfo.email",
        "openid",
        "https://www.googleapis.com/auth/gmail.readonly",
    ],
    "token_type": "Bearer",
    "id_token": "eyJhbGciOiJSUzI1NiIsImtpZCI6ImEzYjc2MmY4NzFjZGIzYmFlMDA0NGM2NDk2MjJmYzEzOTZlZGEzZTMiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiI2MDQwMDU1NzEtbWlpZTI3Nzl0N3A4MWw2NXVwMjZzYjZkaWgxcTd1b2UuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiI2MDQwMDU1NzEtbWlpZTI3Nzl0N3A4MWw2NXVwMjZzYjZkaWgxcTd1b2UuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMDg5NDA4NTU1NDg2MTU2NDgxOTIiLCJlbWFpbCI6ImNsaWZmLnJvc2VuQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJhdF9oYXNoIjoibGFVMmxldVVBUk1vYm1QU1JPQnQ0QSIsIm5hbWUiOiJDbGlmZiBSb3NlbiIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BQ2c4b2NJSnBLd0o2RlA1WkJzODFfMXhzY0licXFxZUR1b2swbXJGQjl3UWpnY0lRbWNjPXM5Ni1jIiwiZ2l2ZW5fbmFtZSI6IkNsaWZmIiwiZmFtaWx5X25hbWUiOiJSb3NlbiIsImlhdCI6MTcxNTQ2NDA4MywiZXhwIjoxNzE1NDY3NjgzfQ.UeOWvTLfpKzphf9mVTrY9G9kJTVyjJkPIRLJHVXfd0hBKi9V8sMvQop9OgJ23yt4d4wy0BPDV_CEIhQxXFiQueQU8TzrMjIjr6kH0bjTMMKr1PgpUpVhB-VG49QkFo31rAhdTsXDmb2tFm3qM-WuRBUjomkXkRPT_BNLPLJeIOIuarrhTVostaKSG_a4HprAapAzWvYGeL-RqDhHRJEZ-kf6VrHZXWM03w4t7RijKvg_PiLBWN5vdYPHXc4weNOFGNwAoPCp5RhZX4VV_fchTc3tEjoYOLMDqEn65nuGRknS39lLCKQIimy53nYnG0xXM1lx7bQJzIyg_zvYq6ZzJA",
    "expires_at": 1715467683.7838662,
}
