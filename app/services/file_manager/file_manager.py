from app.core.config import INPUT_DIR, OUTPUT_DIR, ARCHIVE_DIR
import shutil
import logging

def get_next_pdf():
    # Find all files ending in .pdf
    pdf_files = list(INPUT_DIR.glob("*.pdf"))

    if not pdf_files:
        logging.warning("No PDFs found in input directory")
        return None

    # Return the first one found
    logging.info("Found {:n} PDFs in input directory".format(len(pdf_files)))
    return pdf_files[0]


def archive_file(file_path):
    # Ensure archive directory exists
    ARCHIVE_DIR.mkdir(exist_ok=True)

    # Move the file
    destination = ARCHIVE_DIR / file_path.name

    # Handle duplicate filenames in archive by appending a timestamp if needed
    if destination.exists():
        destination = ARCHIVE_DIR / f"processed_{file_path.name}"

    shutil.move(str(file_path), str(destination))
    logging.info(f"File moved to archive: {destination}")