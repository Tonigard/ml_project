import pytest
from fastapi.testclient import TestClient

from fraud_detection.config import settings
from fraud_detection.service.app import app


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


def make_payload(value: float = 0.0) -> dict:
    return {name: value for name in settings.FEATURE_LIST}


@pytest.fixture
def valid_payload() -> dict:
    return make_payload(0.5)
