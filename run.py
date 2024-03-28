from utils import openai_wrappers as model
from utils.gmail_api import (
    get_service,
    get_labels,
    get_messages,
    get_message,
    get_message_text,
)

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
    start_date = "2024/03/05"
    end_date = "2024/03/07"
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


main()
