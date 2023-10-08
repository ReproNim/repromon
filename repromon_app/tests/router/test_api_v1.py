import logging

from fastapi.testclient import TestClient

from repromon_app.dao import DAO
from repromon_app.model import (DataProviderId, MessageCategoryId,
                                MessageLevelId)

logger = logging.getLogger(__name__)
logger.debug(f"name={__name__}")


def test_account_get_roles(
        test_client: TestClient,
        oauth2_admin_headers
):
    response = test_client.get(
        "/api/1/account/get_roles",
        headers=oauth2_admin_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_account_get_user(
        test_client: TestClient,
        oauth2_admin_headers
):
    response = test_client.get(
        "/api/1/account/get_user",
        params={"username": "admin"},
        headers=oauth2_admin_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "admin"


def test_account_get_users(
        test_client: TestClient,
        oauth2_admin_headers
):
    response = test_client.get(
        "/api/1/account/get_users",
        headers=oauth2_admin_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


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


def test_feedback_get_message(
        test_client: TestClient,
        oauth2_tester1_headers
):
    response = test_client.get(
        "/api/1/feedback/get_message",
        params={"message_id": -1},
        headers=oauth2_tester1_headers)
    assert response.status_code == 200
    data = response.json()
    assert data is None


def test_feedback_get_message_log(
        test_client: TestClient,
        oauth2_tester1_headers
):
    response = test_client.get(
        "/api/1/feedback/get_message_log",
        headers=oauth2_tester1_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_feedback_get_study_header(
        test_client: TestClient,
        oauth2_tester1_headers
):
    response = test_client.get(
        "/api/1/feedback/get_study_header",
        params={"study_id": -1},
        headers=oauth2_tester1_headers)
    assert response.status_code == 200
    data = response.json()
    assert data is None


def test_login_get_current_user(
        test_client: TestClient,
        oauth2_tester1_headers
):
    response = test_client.get(
        "/api/1/login/get_current_user",
        headers=oauth2_tester1_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "tester1"


def test_message_send_message(
        test_client: TestClient,
        apikey_tester2_headers
):
    response = test_client.post(
        "/api/1/message/send_message",
        params={
            "study": "Test Study Name",
            "category": int(MessageCategoryId.FEEDBACK),
            "level": int(MessageLevelId.INFO),
            "device": 1,
            "provider": int(DataProviderId.MRI),
            "description": "Test message from test_api_v1",
            "payload": "{'foobar': 111}"

        },
        headers=apikey_tester2_headers)
    assert response.status_code == 200
    data = response.json()
    msg2 = DAO.message.get_message_log_info(data["id"])
    assert msg2


def test_secsys_calculate_apikey(
        test_client: TestClient,
        oauth2_admin_headers
):
    response = test_client.get(
        "/api/1/secsys/calculate_apikey",
        params={"apikey_data": "data321987655667132a"},
        headers=oauth2_admin_headers)
    assert response.status_code == 200
    assert response.text


def test_secsys_create_access_token(
        test_client: TestClient,
        oauth2_admin_headers
):
    response = test_client.get(
        "/api/1/secsys/create_access_token",
        params={"username": "tester1", "expire_sec": 1},
        headers=oauth2_admin_headers)
    assert response.status_code == 200
    assert response.json()["access_token"]


def test_secsys_create_apikey(
        test_client: TestClient,
        oauth2_admin_headers
):
    response = test_client.get(
        "/api/1/secsys/create_apikey",
        headers=oauth2_admin_headers)
    assert response.status_code == 200
    assert response.json()["key"]


def test_secsys_get_all_apikeys(
        test_client: TestClient,
        oauth2_admin_headers
):
    response = test_client.get(
        "/api/1/secsys/get_all_apikeys",
        headers=oauth2_admin_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_secsys_get_apikey_hash(
        test_client: TestClient,
        oauth2_admin_headers
):
    response = test_client.get(
        "/api/1/secsys/get_apikey_hash",
        params={"apikey": "Axsdsd.as455t65fbcZXZXzxzxsvfvgffd"},
        headers=oauth2_admin_headers)
    assert response.status_code == 200
    h = response.json()["apikey_hash"]
    assert h == "Axsdsd_nzwpPMm2EV9G6hNZuj3R49G4Wrj0y8BsAmuMUHTi1mE="


def test_secsys_get_password_hash(
        test_client: TestClient,
        oauth2_admin_headers
):
    response = test_client.get(
        "/api/1/secsys/get_password_hash",
        params={"password": "sfegfvvfd&%6s"},
        headers=oauth2_admin_headers)
    assert response.status_code == 200
    assert response.json()["password_hash"]


def test_secsys_get_user_apikey(
        test_client: TestClient,
        apikey_tester1,
        oauth2_admin_headers
):
    response = test_client.get(
        "/api/1/secsys/get_user_apikey",
        params={"username": "tester1"},
        headers=oauth2_admin_headers)
    assert response.status_code == 200
    assert response.json()["apikey"] == apikey_tester1


def test_secsys_get_user_devices(
        test_client: TestClient,
        oauth2_admin_headers
):
    response = test_client.get(
        "/api/1/secsys/get_user_devices",
        params={"username": "tester1"},
        headers=oauth2_admin_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_secsys_get_user_roles(
        test_client: TestClient,
        oauth2_admin_headers
):
    response = test_client.get(
        "/api/1/secsys/get_user_roles",
        params={"username": "tester1"},
        headers=oauth2_admin_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_secsys_get_users_by_role(
        test_client: TestClient,
        oauth2_admin_headers
):
    response = test_client.get(
        "/api/1/secsys/get_users_by_role",
        params={"rolename": "admin"},
        headers=oauth2_admin_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_secsys_get_username_by_apikey(
        test_client: TestClient,
        apikey_tester1,
        oauth2_admin_headers
):
    response = test_client.get(
        "/api/1/secsys/get_username_by_apikey",
        params={"apikey": apikey_tester1},
        headers=oauth2_admin_headers)
    assert response.status_code == 200
    assert response.json()["username"] == "tester1"


def test_secsys_get_username_by_token(
        test_client: TestClient,
        token_tester1,
        oauth2_admin_headers
):
    response = test_client.get(
        "/api/1/secsys/get_username_by_token",
        params={"token": token_tester1},
        headers=oauth2_admin_headers)
    assert response.status_code == 200
    assert response.json()["username"] == "tester1"
