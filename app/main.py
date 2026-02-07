import logging

from app.services.file_manager.file_manager import get_next_pdf, archive_files
from services.pdf_to_csv import main as pdf_to_csv
from services.push_csv import main as push_csv
import services.file_manager as file_manager

def run_pipeline():

    #TODO iterate through all files in input folder
    pdf_path = get_next_pdf()

    generated_csv_path = pdf_to_csv(pdf_to_convert=pdf_path)

    if generated_csv_path:
        push_csv(file_to_upload=generated_csv_path)

    #TODO add archiving step for all input and output folders
    archive_files()

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,  # Set minimum log level
        format="%(asctime)s %(levelname)s %(message)s",
    )
    run_pipeline()