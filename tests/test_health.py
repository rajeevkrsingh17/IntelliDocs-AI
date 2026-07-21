import sys
from pathlib import Path
from fastapi.testclient import TestClient

# Add scripts directory to Python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT / "scripts"))
sys.path.append(str(PROJECT_ROOT))

from scripts.api import app

client = TestClient(app)


def test_api_health():
    """
    Test that the root endpoint is running and returns status.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "status": "running",
        "message": "IntelliDocs AI Backend Running",
    }
