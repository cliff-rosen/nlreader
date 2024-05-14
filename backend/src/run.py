from utils import openai_wrappers as model
from utils.gmail_api import (
    get_service_from_JWT,
    get_labels,
    get_messages,
    get_message,
    get_message_text,
)
from utils import gmail_api, utils
from utils import db

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

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NfdG9rZW4iOiJ5YTI5LmEwQVhvb0NndDJpaFpWcS1iV3BaLWZHYXlEM1dFRGFYTXVDcGVHRlVhVHpxYk55aHVmeEgzdGRrV2pjQzhWaUJ4aUJ1TXEwVW9iRm1oV18xa2VyWTBHRUVvdXVkUnNaenJVTTJfeWpNTVN6T1lBWWJTQXZrZkdzMEdBWUhTOFBrM3JZeWs4OWhxTUlfN05rUG9Sa3YweGJUbGMybTNaVHp0bEc4T3hhQ2dZS0FWZ1NBUkFTRlFIR1gyTWlCd1U3LVNOb1F2VVZGUkpZNUtFV0p3MDE3MSIsInJlZnJlc2hfdG9rZW4iOiIxLy8wNHNMVHpyd2psdVVWQ2dZSUFSQUFHQVFTTmdGLUw5SXJlWndweWkxM3J5cWUtbERMNkJ1UVg5RnA5Ui1wSUJfb19SUExGLXVJZ2VGQTNHNndteHNUbE9udER2U2ZSRjJzUXciLCJzdWIiOiIxMDg5NDA4NTU1NDg2MTU2NDgxOTIifQ.dxxpKK_k4YnVLw46pULJBCsD96J3E7oL8jtOhZFZduU"
token_obj = utils.decode_google_jwt(token)
print(token_obj)

"""
user_email = "cliff@abc.com"
user_id_google = "google_12345"
user_first_name = "Cliff"
user_last_name = "Rosen"

user_id = db.insert_user(user_email, user_id_google, user_first_name, user_last_name)
print(user_id)

user = db.get_user_by_google_user_id("google_112345")
print(user)
"""
