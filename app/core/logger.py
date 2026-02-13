import logging
from app.core.config import LOG_FILE_PATH

def setup_logger() :
        logging.basicConfig(
        level=logging.INFO,  # Set minimum log level
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE_PATH),  # Saves to file
            logging.StreamHandler() # Print to terminal
        ]
    )
