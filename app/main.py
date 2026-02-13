import logging
from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager
from  app.core.config import LOG_FILE_PATH, INPUT_DIR, ARCHIVE_DIR, OUTPUT_DIR
from app.api.pipeline_router import router as pipeline_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- STARTUP: Runs before the server starts taking requests ---
    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    logging.info("Pycountant lifespan started: Directories verified.")
    
    yield  # The app is now "running" here
    
    # --- SHUTDOWN: Runs right before the server stops ---
    logging.info("Pycountant lifespan ending.")

app = FastAPI(title="Pycountant API")

app.include_router(pipeline_router, prefix="/api/v1", tags=["Accounting"])

if __name__ == "__main__":

    uvicorn.run(
        "main:app", 
        host="127.0.0.1", 
        port=8000, 
        reload=True  # Auto-restarts when you save code
    )

    # TODO move to loggin class
    logging.basicConfig(
        level=logging.INFO,  # Set minimum log level
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE_PATH),  # Saves to file
            logging.StreamHandler()  # Also prints to your terminal
        ]
    )
