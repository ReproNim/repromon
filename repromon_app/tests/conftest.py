import logging
import threading

import pytest

from repromon_app.config import app_config, app_config_init
from repromon_app.db import db_init
from repromon_app.service import SecSysService

logger = logging.getLogger(__name__)

_apikey_tester1: str = None
_apikey_tester2: str = None
_apikey_tester3: str = None


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
