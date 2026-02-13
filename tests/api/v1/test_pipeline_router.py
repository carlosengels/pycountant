from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)

def test_trigger_pipeline_wrong_method():
    response = client.get("api/v1/run-pipeline")
    assert response.status_code == 405

@patch("app.api.v1.pipeline_router.pdf_to_csv.main")
@patch("app.api.v1.pipeline_router.push_csv.main")
def test_run_pipeline_full_flow(mock_push, mock_convert):
    """
    Test the pipeline trigger without touching real files or networks.
    """
    # 1. Setup Mock behavior
    # We tell the mocks what they should 'return' when called
    mock_convert.return_value = "/tmp/test_output.csv"
    mock_push.return_value = True

    # 2. Action: Trigger the API
    response = client.post("/api/v1/run-pipeline")

    # 3. Assertions
    assert response.status_code == 200
    assert response.json()["status"] == "Pipeline started"

    # 4. Verification: Did the router actually call our services?
    mock_convert.assert_called_once()
    mock_push.assert_called_once_with(file_to_upload="/tmp/test_output.csv")