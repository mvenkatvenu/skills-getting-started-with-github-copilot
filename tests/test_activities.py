from pathlib import Path
import sys

# Ensure `src` is on path so we can import the FastAPI `app`
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from app import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_get_activities():
    res = client.get("/activities")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, dict)
    # Basic sanity: a known activity exists
    assert "Chess Club" in data


def test_signup_and_unregister():
    activity = "Chess Club"
    email = "teststudent@example.com"

    # Sign up
    res = client.post(f"/activities/{activity}/signup?email={email}")
    assert res.status_code == 200
    assert email in client.get("/activities").json()[activity]["participants"]

    # Duplicate signup should fail
    res_dup = client.post(f"/activities/{activity}/signup?email={email}")
    assert res_dup.status_code == 400

    # Unregister
    res_un = client.post(f"/activities/{activity}/unregister?email={email}")
    assert res_un.status_code == 200
    assert email not in client.get("/activities").json()[activity]["participants"]

    # Unregister again should fail
    res_un2 = client.post(f"/activities/{activity}/unregister?email={email}")
    assert res_un2.status_code == 400
