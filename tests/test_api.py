import uuid

import pytest

from conftest import make_payload
from fraud_detection.service.app import app

URL = "/v1/predict"

def test_extra_field_returns_422(client, valid_payload):
    r = client.post(URL, json={**valid_payload, "junk": 1})
    assert r.status_code == 422


def test_missing_field_returns_422(client, valid_payload):
    first = next(iter(valid_payload))
    del valid_payload[first]
    r = client.post(URL, json=valid_payload)
    assert r.status_code == 422


@pytest.mark.parametrize("garbage", ["abc", None, [1, 2], {"a": 1}])
def test_garbage_value_returns_422(client, valid_payload, garbage):
    first = next(iter(valid_payload))
    r = client.post(URL, json={**valid_payload, first: garbage})
    assert r.status_code == 422


def test_non_json_body_returns_422(client):
    r = client.post(URL, content=b"not json", headers={"Content-Type": "application/json"})
    assert r.status_code == 422


def test_empty_body_returns_422(client):
    r = client.post(URL, json={})
    assert r.status_code == 422


# Smoke

def test_health_and_ready(client):
    assert client.get("/health").status_code == 200
    r = client.get("/ready")
    assert r.status_code == 200
    assert r.json() == {"status": "ready"}


def test_predict_smoke(client, valid_payload):
    r = client.post(URL, json=valid_payload)
    assert r.status_code == 200
    body = r.json()

    assert isinstance(body["score"], float)
    assert 0.0 <= body["score"] <= 1.0
    assert isinstance(body["fraud"], bool)
    assert isinstance(body["model_version"], str) and body["model_version"]
    uuid.UUID(body["request_id"])  # упадёт, если это не UUID
    assert isinstance(body["latency_ms"], (int, float)) and body["latency_ms"] >= 0


def test_fraud_matches_threshold(client, valid_payload):
    body = client.post(URL, json=valid_payload).json()
    threshold = app.state.meta["threshold"]
    assert body["fraud"] == (body["score"] >= threshold)


# Детерминизм

def test_same_input_same_output(client, valid_payload):
    a = client.post(URL, json=valid_payload).json()
    b = client.post(URL, json=valid_payload).json()

    assert a["score"] == b["score"]
    assert a["fraud"] == b["fraud"]
    assert a["model_version"] == b["model_version"]
    assert a["request_id"] != b["request_id"]  # id у каждого запроса свой


@pytest.mark.parametrize("value", [-1.0, 0.0, 1.0, 1000.0])
def test_deterministic_on_different_inputs(client, value):
    payload = make_payload(value)
    scores = [client.post(URL, json=payload).json()["score"] for _ in range(3)]
    assert len(set(scores)) == 1
