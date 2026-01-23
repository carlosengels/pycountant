import os.path
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from google.oauth2 import service_account

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SERVICE_ACCOUNT_FILE = '/artifacts/keys.json'

# The ID
SAMPLE_SPREADSHEET_ID = "1Oa_ql0Ft2qJHULWxVCIN9lsSdEBAEViM_Ix2Ucs40aU"
SAMPLE_RANGE_NAME = "monthly_statement_12-13-25.csv!a1:g45"

def main():
  creds = None
  creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)


  # If there are no (valid) credentials available, let the user log in.
  service = build("sheets", "v4", credentials=creds)

  # Call the Sheets API
  sheet = service.spreadsheets()
  result = (
      sheet.values()
      .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME)
      .execute()
  )
  values = result.get("values", [])

  if not values:
    print("No data found.")
    return
  print(values)

if __name__ == "__main__":
  main()