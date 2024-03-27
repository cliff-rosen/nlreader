from gmail_api import (
    get_service,
    get_labels,
    get_messages,
    get_message,
    get_message_text,
)


def main():
    service = get_service()
    label = "Label_2689345936544895630"
    start_date = "2024/03/25"
    end_date = "2024/03/26"
    messages = get_messages(service, label, start_date, end_date)
    messages = messages[:1]

    if not messages:
        print("No messages found.")

    for message_part in messages:
        message = get_message(service, message_part["id"])
        print(f"Message ID: {message['msg']['id']}, Subject: {message['subject']}")
        print(message["text"])


main()
