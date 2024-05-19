from utils import openai_wrappers as model
from utils.gmail_api import (
    get_labels,
    get_messages,
    get_message,
    get_message_text,
)
from utils import gmail_api, utils
from utils import db
import json

DELIM = "=================================================================\n"
INSTRUCTION = "Read all stories from the text in the following collection of newsletter emails. Ignore all links.  Then generate a summary in the form of bullets for all key stories, one bullet per key story. If the same story or story theme appears several times consolidate all relevant info in a single bullet:\n\n"


def write_text_to_file(filename, text):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(text)


def main():
    user = db.get_user_by_google_user_id("108940855548615648192")
    creds_dict = json.loads(user["credentials"])
    creds = gmail_api.credentials_from_dict(creds_dict)
    service = gmail_api.get_service_from_creds(creds)

    label = "Label_2689345936544895630"
    start_date = "2024/05/15"
    end_date = "2024/05/16"
    messages = get_messages(service, label, start_date, end_date)
    # messages = messages[:1]

    if not messages:
        print("No messages found.")

    news_text = DELIM
    for message_part in messages:
        message = get_message(service, message_part["id"])
        print(f"Message ID: {message['msg']['id']}, Subject: {message['subject']}")
        news_text += DELIM + message["text"]

    # write_text_to_file("articles.txt", news_text)

    # prompt_messages = messages = [
    #     {"role": "system", "content": "You are a helpful assistant."},
    #     {
    #         "role": "user",
    #         "content": INSTRUCTION + news_text,
    #     },
    # ]

    # res = model.generate(prompt_messages)
    # write_text_to_file("summary.txt", res)

    print("done")


user = db.get_user_by_google_user_id("108940855548615648192")
creds_dict = json.loads(user["credentials"])
creds = gmail_api.credentials_from_dict(creds_dict)
service = gmail_api.get_service_from_creds(creds)

message_id = "18f87b8a4882946b"
# message_id = "18f8753e1c6bedc6"
message = get_message(service, message_id)
print(message["body"])

"""
 * Detected change in 'C:\\Users\\cliff\\AppData\\Local\\Packages\\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\\LocalCache\\local-packages\\Python311\\site-packages\\werkzeug\\utils.py', reloading
 * Detected change in 'C:\\Users\\cliff\\AppData\\Local\\Packages\\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\\LocalCache\\local-packages\\Python311\\site-packages\\werkzeug\\datastructures\\__init__.py', reloading
 * Detected change in 'c:\\code\\nlreader\\backend\\src\\utils\\utils.py', reloading
 """
