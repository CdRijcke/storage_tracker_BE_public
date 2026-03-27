# import pytest

from fastapi.testclient import TestClient
from sqlmodel import Session
from storage_tracker.main import app

from storage_tracker.main import get_session


def test_read_product(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)

    response = client.get("/product/peanutbutter", headers={"X-Token": "coneofsilence"})

    assert response.status_code == 200
    assert response.json() == {
        "id": None,
        "name": "peanutbutter",
        "quantity": 2,
        "present": True
    }
