from fastapi import APIRouter, BackgroundTasks
from app.services.pdf_to_csv import pdf_to_csv
from app.services.push_csv import push_csv
from app.services.file_manager.file_manager import get_next_pdf, archive_files

router = APIRouter()

@router.get("/health")
async def health_check():
    return {"status": "OK"}

@router.post("/run-pipeline")
async def trigger_pipeline(background_tasks: BackgroundTasks):
    background_tasks.add_task(run_pipeline)
    return {"status": "Pipeline started", "message": "Pycountant is working in the background."}

def run_pipeline():

    pdf_path = get_next_pdf()

    generated_csv_path = pdf_to_csv.main(pdf_to_convert=pdf_path)
    if generated_csv_path:
        push_csv.main(file_to_upload=generated_csv_path)

    archive_files()