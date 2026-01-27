from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ARTIFACTS_DIR = BASE_DIR / "artifacts"
INPUT_DIR = ARTIFACTS_DIR / "input"
OUTPUT_DIR = ARTIFACTS_DIR / "output"
ARCHIVE_DIR = ARTIFACTS_DIR / "archive"