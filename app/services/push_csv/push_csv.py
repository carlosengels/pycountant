
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd
from google.oauth2 import service_account
from app.core.config import ARTIFACTS_DIR
import sys

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SERVICE_ACCOUNT_FILE = ARTIFACTS_DIR / "keys.json"
SPREADSHEET_ID = "1Oa_ql0Ft2qJHULWxVCIN9lsSdEBAEViM_Ix2Ucs40aU"

def csv_to_list (local_csv_path) :
  filename = local_csv_path
  df = pd.read_csv(filename)
  csv_headers = df.columns.values.tolist()
  csv_content = df.fillna('').values.tolist()
  csv_content.insert(0, csv_headers)
  print(csv_content)
  return csv_content

def main(file_to_upload):
# Google Sheets API set-up
  creds = None
  creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
  service = build("sheets", "v4", credentials=creds)
  sheet = service.spreadsheets()

# Create new sheet
  try:
    create_sheet_body = {
      "requests": {
        "addSheet": {
          "properties": {
            "title": file_to_upload
          }
        }
      }
    }
    sheet.batchUpdate(spreadsheetId=SPREADSHEET_ID, body=create_sheet_body).execute()

    local_csv = str(ARTIFACTS_DIR / file_to_upload) + ".csv"
    csv_data = csv_to_list(local_csv)
    sheet.values().update(spreadsheetId=SPREADSHEET_ID, range=file_to_upload+"!A1", valueInputOption="USER_ENTERED", body={"values":csv_data}).execute()

  except HttpError as err:
    print(err)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        target_file = sys.argv[1]
        main(file_to_upload=target_file)
    else:
        print("Error: Please provide a file path. Example: python push_csv.py data.csv")