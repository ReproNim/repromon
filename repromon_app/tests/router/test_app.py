import logging

from fastapi.testclient import TestClient

logger = logging.getLogger(__name__)
logger.debug(f"name={__name__}")


def test_app_root(test_client: TestClient):
    logger.debug("test_app_root()")
    response = test_client.get("/")
    assert response.status_code == 200
    assert "ReproMon Home" in response.text
