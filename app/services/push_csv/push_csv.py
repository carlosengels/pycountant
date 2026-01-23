
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd
from google.oauth2 import service_account
from app.core.config import ARTIFACTS_DIR


SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SERVICE_ACCOUNT_FILE = ARTIFACTS_DIR / "keys.json"
NEW_SHEET_NAME = "TEST4"
LOCAL_CSV = ARTIFACTS_DIR / "monthly_statement_12-13-25.csv"
SAMPLE_SPREADSHEET_ID = "1Oa_ql0Ft2qJHULWxVCIN9lsSdEBAEViM_Ix2Ucs40aU"

def csv_to_list (local_csv_path) :
  filename = local_csv_path
  df = pd.read_csv(filename)
  csv_headers = df.columns.values.tolist()
  csv_content = df.fillna('').values.tolist()
  csv_content.insert(0, csv_headers)
  print(csv_content)
  return csv_content

def main():
  creds = None
  creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
  service = build("sheets", "v4", credentials=creds)
  sheet = service.spreadsheets()

  try:
    create_sheet_body = {
      "requests": {
        "addSheet": {
          "properties": {
            "title": NEW_SHEET_NAME
          }
        }
      }
    }
    sheet.batchUpdate(spreadsheetId=SAMPLE_SPREADSHEET_ID, body=create_sheet_body).execute()

    csv_data = csv_to_list(LOCAL_CSV)
    sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="TEST4!A1", valueInputOption="USER_ENTERED", body={"values":csv_data}).execute()

  except HttpError as err:
    print(err)


if __name__ == "__main__":
  main()