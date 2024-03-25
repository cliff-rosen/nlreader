import getpass
from datetime import datetime

from gmail_api_2 import get_emails_by_label_date_range
from theme_analysis import analyze_themes
from report_generation import generate_report


def main():
  """
  Main function to orchestrate the program flow.
  """
 
  # Get user input
  label_name = input("Enter the Gmail label name for tech newsletters: ")
  start_date_str = input("Enter start date (YYYY-MM-DD): ")
  end_date_str = input("Enter end date (YYYY-MM-DD): ")

  # Validate and convert dates (add error handling for invalid format)
  try:
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
  except ValueError:
    print("Invalid date format. Please use YYYY-MM-DD.")
    return

  # Get Gmail credentials securely (consider using a secure credential store)
  username = input("Enter your Gmail username: ")
  password = getpass.getpass("Enter your Gmail password: ")

  # Retrieve emails using gmail_api.py
  print("Retrieving emails...")
  emails = get_emails_by_label_date_range(username, password, label_name, start_date, end_date)
  for email in emails:
    print(email)

  # Analyze themes using theme_analysis.py
  print("Analyzing themes...")
  # themes, keywords = analyze_themes(emails)

  # Generate report using report_generation.py
  print("Generating report...")
  # generate_report(themes, keywords, start_date, end_date)

  print("Analysis complete! The report has been generated.")

'''
if __name__ == "__main__":
  main()
'''