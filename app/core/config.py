from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ARTIFACTS_DIR = BASE_DIR / "artifacts"

#PDF and CSV handling
INPUT_DIR = ARTIFACTS_DIR / "input"
OUTPUT_DIR = ARTIFACTS_DIR / "output"
ARCHIVE_DIR = ARTIFACTS_DIR / "archive"

#Logging
LOG_DIR = ARTIFACTS_DIR / "logs"
LOG_FILE_PATH = LOG_DIR / "pycountant.log"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE_PATH.touch(exist_ok=True)

