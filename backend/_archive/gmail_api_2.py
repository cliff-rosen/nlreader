from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client.service_account import ServiceAccountCredentials

def get_emails_by_label_date_range(username, password, label_name, start_date, end_date):
  """
  Connects to Gmail API using OAuth and retrieves emails based on criteria.

  Args:
      username: Gmail username for authentication.
      password: Gmail password for authentication.
      label_name: Name of the label containing tech newsletters.
      start_date: Start date for the date range (datetime.date object).
      end_date: End date for the date range (datetime.date object).

  Returns:
      A list of dictionaries representing the retrieved emails.
  """

  # Replace with path to your service account key file (for production)
  credentials = ServiceAccountCredentials.from_json_keyfile_name(
      'path/to/your/service_account.json', scopes=['https://www.googleapis.com/auth/gmail.readonly'])

  # Uncomment for username/password authentication (less secure for production)
  # http = Http()
  # credentials = credentials.authorize(http)

  service = build('gmail', 'v1', credentials=credentials)

  # Define search query based on label and date range
  query = f'label:{label_name} after:{start_date.strftime("%Y/%m/%d")} before:{end_date.strftime("%Y/%m/%d")}'

  try:
    # Retrieve email list matching the search query
    results = service.users().messages().list(userId='me', q=query).execute()
    messages = results.get('messages', [])

    # Extract relevant data from each message
    emails = []
    for msg in messages:
      # Use message id to get full details of each email (optional)
      # email_data = service.users().messages().get(userId='me', id=msg['id']).execute()
      emails.append({'id': msg['id']})  # Currently, only storing message ID

    return emails

  except Exception as e:
    print(f"An error occurred: {e}")
    return []

