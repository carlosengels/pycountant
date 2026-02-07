import logging

from app.services.file_manager.file_manager import get_next_pdf, archive_files
from services.pdf_to_csv import main as pdf_to_csv
from services.push_csv import main as push_csv
from  app.core.config import LOG_FILE_PATH

def run_pipeline():

    pdf_path = get_next_pdf()

    generated_csv_path = pdf_to_csv(pdf_to_convert=pdf_path)
    if generated_csv_path:
        push_csv(file_to_upload=generated_csv_path)

    archive_files()

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,  # Set minimum log level
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE_PATH),  # Saves to file
            logging.StreamHandler()  # Also prints to your terminal
        ]
    )
    run_pipeline()