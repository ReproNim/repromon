import logging

from fastapi.testclient import TestClient

logger = logging.getLogger(__name__)
logger.debug(f"name={__name__}")


def test_admin_root(
        test_client: TestClient,
        admin_basic_auth
):
    response = test_client.get("/admin", auth=admin_basic_auth)
    assert response.status_code == 200
    assert "ReproMon Admin Home" in response.text
