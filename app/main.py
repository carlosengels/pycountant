import logging
from services.pdf_to_csv import main as pdf_to_csv
from services.push_csv import main as push_csv

def run_pipeline():
    generated_csv_path = pdf_to_csv()
    # generated_csv_path = "monthly_statement_12-13-25.csv"
    if generated_csv_path:
        push_csv(file_to_upload=generated_csv_path)

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,  # Set minimum log level
        format="%(asctime)s %(levelname)s %(message)s",
    )
    run_pipeline()