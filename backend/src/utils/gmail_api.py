import google.oauth2.credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import os, pickle
import base64
from flask import session, redirect, url_for
from datetime import datetime, timedelta

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
    messages = []
    message_list = get_message_list(service, label, start_date, end_date)

    for message_part in message_list:
        message = get_message(service, message_part["id"])
        print(f"Message ID: {message['msg']['id']}, Subject: {message['subject']}")
        messages.append(
            {
                "key": message["msg"]["id"],
                "date": message["date"],
                "sender": message["sender"],
                "subject": message["subject"],
                "body": message["body"][:50],
            }
        )
    return messages


def get_message_list(service, label, start_date, end_date):

    end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
    next_day = end_date_obj + timedelta(days=1)
    next_day_str = next_day.strftime("%Y-%m-%d")
    query = f"after:{start_date} before:{next_day_str}"

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
    date = next(
        (header["value"] for header in headers if header["name"] == "Date"),
        "No Date",
    )
    sender = next(
        (header["value"] for header in headers if header["name"] == "From"),
        "UNKOWN",
    )
    subject = next(
        (header["value"] for header in headers if header["name"] == "Subject"),
        "No Subject",
    )
    text = get_message_text(msg)
    return {
        "msg": msg,
        "date": date,
        "sender": sender,
        "subject": subject,
        "body": text,
    }


def get_message_text(message):
    print("entered get_message_text")
    try:
        payload = message.get("payload", {})

        if payload.get("mimeType") == "text/plain":
            # Body is directly in payload
            print(" message payload of type text/plain")
            return base64.urlsafe_b64decode(data.encode("ASCII")).decode("utf-8")
        elif payload.get("mimeType").startswith("multipart/"):
            print(" message payload of type multipart/")
            parts = payload.get("parts", [])
            # print("payload:", payload)
            text = ""
            for part in parts:
                print(f" processing part {part['partId']} of type {part['mimeType']}")
                if part["mimeType"] == "text/plain":
                    data = part["body"]["data"]
                    data_decoded = base64.urlsafe_b64decode(
                        data.encode("ASCII")
                    ).decode("utf-8")
                    # print(part["mimeType"])
                    # print(data_decoded[:100])
                    text += data_decoded
            if text:
                return text
            else:
                return "No text body found"
        else:
            return "No text body found"

    except Exception as e:
        print("error", e)
        text = "ERROR"
    return "No text body found"


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


"""
https://developers.google.com/resources/api-libraries/documentation/gmail/v1/python/latest/gmail_v1.users.messages.html

    { # An email message.
    "internalDate": "A String", # The internal message creation timestamp (epoch ms), which determines ordering in the inbox. For normal SMTP-received email, this represents the time the message was originally accepted by Google, which is more reliable than the Date header. However, for API-migrated mail, it can be configured by client to be based on the Date header.
    "historyId": "A String", # The ID of the last history record that modified this message.
    "payload": { # A single MIME message part. # The parsed email structure in the message parts.
      "body": { # The body of a single MIME message part. # The message part body for this part, which may be empty for container MIME message parts.
        "data": "A String", # The body data of a MIME message part as a base64url encoded string. May be empty for MIME container types that have no message body or when the body data is sent as a separate attachment. An attachment ID is present if the body data is contained in a separate attachment.
        "attachmentId": "A String", # When present, contains the ID of an external attachment that can be retrieved in a separate messages.attachments.get request. When not present, the entire content of the message part body is contained in the data field.
        "size": 42, # Number of bytes for the message part data (encoding notwithstanding).
      },
      "mimeType": "A String", # The MIME type of the message part.
      "partId": "A String", # The immutable ID of the message part.
      "filename": "A String", # The filename of the attachment. Only present if this message part represents an attachment.
      "headers": [ # List of headers on this message part. For the top-level message part, representing the entire message payload, it will contain the standard RFC 2822 email headers such as To, From, and Subject.
        {
          "name": "A String", # The name of the header before the : separator. For example, To.
          "value": "A String", # The value of the header after the : separator. For example, someuser@example.com.
        },
      ],
      "parts": [ # The child MIME message parts of this part. This only applies to container MIME message parts, for example multipart/*. For non- container MIME message part types, such as text/plain, this field is empty. For more information, see RFC 1521.
        # Object with schema name: MessagePart
      ],
    },
    "snippet": "A String", # A short part of the message text.
    "raw": "A String", # The entire email message in an RFC 2822 formatted and base64url encoded string. Returned in messages.get and drafts.get responses when the format=RAW parameter is supplied.
    "sizeEstimate": 42, # Estimated size in bytes of the message.
    "threadId": "A String", # The ID of the thread the message belongs to. To add a message or draft to a thread, the following criteria must be met:
        # - The requested threadId must be specified on the Message or Draft.Message you supply with your request.
        # - The References and In-Reply-To headers must be set in compliance with the RFC 2822 standard.
        # - The Subject headers must match.
    "labelIds": [ # List of IDs of labels applied to this message.
      "A String",
    ],
    "id": "A String", # The immutable ID of the message.
  }
"""
