from utils import openai_wrappers as model
from utils.gmail_api import (
    get_service_from_JWT,
    get_labels,
    get_messages,
    get_message,
    get_message_text,
)
from utils import gmail_api
from jwt import JWT


DELIM = "=================================================================\n"
INSTRUCTION = "Read all stories from the text in the following collection of newsletter emails. Ignore all links.  Then generate a summary in the form of bullets for all key stories, one bullet per key story. If the same story or story theme appears several times consolidate all relevant info in a single bullet:\n\n"


def write_text_to_file(filename, text):
    """
    Creates a new file with the specified filename and writes the provided text to it.

    Parameters:
    filename (str): The name of the file to create.
    text (str): The text to write into the file.
    """
    with open(filename, "w", encoding="utf-8") as file:
        file.write(text)


def main():
    service = get_service()
    label = "Label_2689345936544895630"
    start_date = "2024/04/15"
    end_date = "2024/04/22"
    messages = get_messages(service, label, start_date, end_date)
    # messages = messages[:1]

    if not messages:
        print("No messages found.")

    news_text = DELIM
    for message_part in messages:
        message = get_message(service, message_part["id"])
        print(f"Message ID: {message['msg']['id']}, Subject: {message['subject']}")
        # print(message["text"])
        news_text += DELIM + message["text"]

    write_text_to_file("articles.txt", news_text)

    prompt_messages = messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": INSTRUCTION + news_text,
        },
    ]

    res = model.generate(prompt_messages)
    write_text_to_file("summary.txt", res)

    print("done")


"""
service = get_service()
if 1:
    label = "Label_2689345936544895630"
    start_date = "2024/04/15"
    end_date = "2024/04/22"
    messages = get_messages(service, label, start_date, end_date)
    print(messages)
"""

jwt = JWT()
g_jwt = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImEzYjc2MmY4NzFjZGIzYmFlMDA0NGM2NDk2MjJmYzEzOTZlZGEzZTMiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiI2MDQwMDU1NzEtbWlpZTI3Nzl0N3A4MWw2NXVwMjZzYjZkaWgxcTd1b2UuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiI2MDQwMDU1NzEtbWlpZTI3Nzl0N3A4MWw2NXVwMjZzYjZkaWgxcTd1b2UuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMDg5NDA4NTU1NDg2MTU2NDgxOTIiLCJlbWFpbCI6ImNsaWZmLnJvc2VuQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJhdF9oYXNoIjoiN1NSbnFDWU95SFZ2M3k1TmtSa1pRUSIsIm5hbWUiOiJDbGlmZiBSb3NlbiIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BQ2c4b2NJSnBLd0o2RlA1WkJzODFfMXhzY0licXFxZUR1b2swbXJGQjl3UWpnY0lRbWNjPXM5Ni1jIiwiZ2l2ZW5fbmFtZSI6IkNsaWZmIiwiZmFtaWx5X25hbWUiOiJSb3NlbiIsImlhdCI6MTcxNTYyMzM1NSwiZXhwIjoxNzE1NjI2OTU1fQ.cvRhlfRa4PQzhbrosGMbHdEM7Z4PQbo9_YZVg0b_B1_CIaRwAIF-cl1NqX1fnOVOqRg6qSs2_0Fvk5q2BZaEbVXz0l1WgWeoFDIzJZ6s1LjDpvMe_z827bM8TNtSnLrkEk9vIptETZCx8wSmXTRJdb-wRtiNJO0JUaXDupxR_mBdXm6Ps8zIthD7cSiEErhISqtJsA3eIsVQ_IgYXSDElZflGBkh9mGSmQYJ-X1unobCC-yeaIdD5VkmPrM1slSu4bRjkha4wKk0t25SqtjCnAFkEfzW0z4e83HBOLVLhunODZ3ZZtVNIaz5bVu05FaYlSyIFVVd4LBR0WaGaGEk2g"
g_token = jwt.decode(g_jwt, do_verify=False)
print(g_token)
