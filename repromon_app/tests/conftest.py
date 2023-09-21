import logging

import pytest

from repromon_app.config import app_config_init

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session", autouse=True)
def init_config():
    logger.debug("init_config()")
    app_config_init()
    yield
