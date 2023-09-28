import logging
import threading

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from httpx import BasicAuth

from repromon_app.config import app_config, app_config_init, app_settings
from repromon_app.db import db_init
from repromon_app.service import SecSysService
from repromon_app.srv import create_fastapi_app

logger = logging.getLogger(__name__)

_apikey_tester1: str = None
_apikey_tester2: str = None
_apikey_tester3: str = None

_fastapi_app: FastAPI = None
_test_client: TestClient = None


@pytest.fixture(scope="session", autouse=True)
def init_config():
    logger.debug("init_config()")
    app_config_init()
    yield


@pytest.fixture(scope="session", autouse=True)
def init_db():
    logger.debug("init_db()")
    logger.debug("Initialize DB...")
    db_init(app_config().db.dict(), threading.get_ident)
    svc: SecSysService = SecSysService()

    global _apikey_tester1, _apikey_tester2, _apikey_tester3
    _apikey_tester1 = svc.get_user_apikey("tester1").apikey
    _apikey_tester2 = svc.get_user_apikey("tester2").apikey
    _apikey_tester3 = svc.get_user_apikey("tester3").apikey
    yield


@pytest.fixture
def admin_basic_auth() -> BasicAuth:
    return BasicAuth("admin", app_settings().INITIAL_ADMIN_PASSWORD)


@pytest.fixture
def apikey_tester1() -> str:
    global _apikey_tester1
    return _apikey_tester1


@pytest.fixture
def apikey_tester2() -> str:
    global _apikey_tester2
    return _apikey_tester2


@pytest.fixture
def apikey_tester3() -> str:
    global _apikey_tester3
    return _apikey_tester3


@pytest.fixture
def base_url() -> str:
    return f"https://{app_settings().WEB_HOST}:{str(app_settings().WEB_PORT)}"


@pytest.fixture
def fastapi_app() -> FastAPI:
    global _fastapi_app
    if not _fastapi_app:
        _fastapi_app = create_fastapi_app()
    return _fastapi_app


@pytest.fixture
def test_client(fastapi_app) -> str:
    global _test_client
    if not _test_client:
        _test_client = TestClient(fastapi_app)
    return _test_client
