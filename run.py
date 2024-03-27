from gmail_api import get_service, get_labels, get_messages, get_message


def main():
    service = get_service()
    label = "Label_2689345936544895630"
    start_date = "2024/03/25"
    end_date = "2024/03/26"
    messages = get_messages(service, label, start_date, end_date)

    if not messages:
        print("No messages found.")

    for message in messages:
        msg = get_message(service, message["id"])
        headers = msg.get("payload", {}).get("headers", [])
        print(headers)
        subject = next(
            (header["value"] for header in headers if header["name"] == "Subject"),
            "No Subject",
        )
        print(f"Message ID: {message['id']}, Subject: {subject}")


main()
