import logging

from fastapi.testclient import TestClient

logger = logging.getLogger(__name__)
logger.debug(f"name={__name__}")


def test_feedback_get_devices(
        test_client: TestClient,
        oauth2_tester1_headers
):
    response = test_client.get(
        "/api/1/feedback/get_devices",
        headers=oauth2_tester1_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["id"] == 1
