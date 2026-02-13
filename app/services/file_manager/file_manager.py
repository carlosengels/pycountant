from app.core.config import INPUT_DIR, OUTPUT_DIR, ARCHIVE_DIR
import shutil
import logging

def get_all_pdf():
    pdf_files = list(INPUT_DIR.glob("*.pdf"))
    logging.info("Found {:n} PDFs in input directory".format(len(pdf_files)))
    if not pdf_files:
        logging.warning("No PDFs found in input directory")
        return None
    
    return pdf_files

def get_next_pdf():
    # Find all files ending in .pdf
    pdf_files = get_all_pdf()
    # Return the first one found
    return pdf_files[0]

# Move all files from input and output to archive
def archive_files():
    ARCHIVE_DIR.mkdir(exist_ok=True, parents=True)
    INPUT_DIR.mkdir(exist_ok=True, parents=True)
    OUTPUT_DIR.mkdir(exist_ok=True, parents=True)

    input_files = list(INPUT_DIR.glob("*.pdf"))
    if input_files:
        for file in input_files:
            destination = ARCHIVE_DIR / f"processed_{file.name}"
            shutil.move(str(file), str(destination))
            logging.info(f"Archived input: {file.name}")
    else:
        logging.info("No input PDF files found to archive.")

    output_files = list(OUTPUT_DIR.glob("*.csv"))
    if output_files:
        for file in output_files:
            destination = ARCHIVE_DIR / f"processed_{file.name}"
            shutil.move(str(file), str(destination))
            logging.info(f"Archived output: {file.name}")


