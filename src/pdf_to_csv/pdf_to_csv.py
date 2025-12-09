from pypdf import PdfReader
import pandas as pd
from io import StringIO
import re
import logging
from pathlib import Path


MODULE_DIR = Path(__file__).resolve().parent
ARTIFACTS_DIR = MODULE_DIR / ".." / ".." / "artifacts"
PDF_PATH = ARTIFACTS_DIR / "Statements.pdf"

ACCOUNT_ACTIVITY_HEADER_CSV = "Date of Transaction,Description,$ Amount,Category,Sub-Category\n"
DATE_FROM_PDF_REGEX = r"(\d{1,2}\/\d{1,2}\/\d{2})\s*-\s*(\d{1,2}\/\d{1,2}\/\d{2})"
ACCOUNT_ACTIVITY_FROM_PDF_REGEX = r"ACCOUNT ACTIVITY.*?\$ Amount\s*(.*?)\s*Total fees charged in"
ACCOUNT_ACTIVITY_LINE_DISSECT_REGEX = r"^(\d{1,2}/\d{1,2})\s+(.+?)\s+(-?\d+\.\d{2})$"

GROCERIES = ("WHOLE", "KING SOOPERS", "EDWARDS")
PETS = ("Pet", "PetCo")
SUBSCRIPTIONS = ("VIX", "Paramount", "Audible", "ESPN", "Spotify")
CAR = ("Conoco", "Phillips 66")

reader = PdfReader(PDF_PATH)


def get_account_activity_str_from_pdf () :
    page = reader.pages[2]
    page_content_str = page.extract_text()
    match = re.search(ACCOUNT_ACTIVITY_FROM_PDF_REGEX,
        page_content_str,
        flags=re.DOTALL
    )
    if match:
        account_activity = match.group(1).strip()
    else:
        account_activity = None
    return account_activity.split("\n")

def get_date_from_pdf () :
    page = reader.pages[0]
    page_content = page.extract_text()
    match = re.search(DATE_FROM_PDF_REGEX, page_content)
    return match.groups()[1].replace("/","-")

def redact (transaction) :
    if "SIMMS" in transaction:
        transaction = "EBAY%"
    return transaction

def categorize (transaction) :
    if any(keyword in transaction.upper() for keyword in GROCERIES):
        return "Groceries"
    if any(keyword in transaction.upper() for keyword in PETS):
        return "Pets"
    if any(keyword in transaction.upper() for keyword in SUBSCRIPTIONS):
        return "Subscriptions"
    if any(keyword in transaction.upper() for keyword in CAR):
        return "Car"
    return ""

def convert_account_activity_content_to_csv (list_of_activity_lines) :
    converted_activity_line_str = ""
    for line in list_of_activity_lines:
        match = re.match(ACCOUNT_ACTIVITY_LINE_DISSECT_REGEX, line)
        if match:
            transaction_date, description, amount = match.groups()
            description = redact(description)
            category = categorize(description)
            statement = transaction_date + "," + description + "," + amount + "," + category + "\n"
            converted_activity_line_str += statement
    logging.info("Converted lines into CSV format.")
    return converted_activity_line_str

def write_to_csv (pdf_content_str, statement_end_date_str) :
    filename = "../artifacts/monthly_statement_{date_str}.csv".format(date_str=statement_end_date_str)
    df = pd.read_csv(StringIO(pdf_content_str))
    df.to_csv(filename, index=False)
    logging.info("Transaction activity saved to {filename}".format(filename=filename))

def main():
    logging.info("Starting main function")
    account_activity_content_csv = convert_account_activity_content_to_csv(get_account_activity_str_from_pdf())
    account_activity_complete_csv = ACCOUNT_ACTIVITY_HEADER_CSV + account_activity_content_csv
    write_to_csv(account_activity_complete_csv, get_date_from_pdf())

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,  # Set minimum log level
        format="%(asctime)s %(levelname)s %(message)s",
    )
    main()