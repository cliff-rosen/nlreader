from gmail_api import get_service


def get_labels():
    service = get_service()
    labels = service.users().labels().list(userId='me').execute().get('labels', [])

    print("about to print")
    for label in labels:
        print(label)

def main():
    service = get_service()

    # get_labels()
    # return

    label = 'Label_2689345936544895630'
    results = service.users().messages().list(userId='me', labelIds=[label], maxResults=5).execute()
    messages = results.get('messages', [])

   
    if not messages:
        print("No messages found.")

    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id'], format='metadata', metadataHeaders=['Subject']).execute()
        headers = msg.get('payload', {}).get('headers', [])
        subject = next((header['value'] for header in headers if header['name'] == 'Subject'), 'No Subject')
        print(f"Message ID: {message['id']}, Subject: {subject}")
          
main()