import logging

from repromon_app.config import app_config, app_settings

logger = logging.getLogger(__name__)
logger.debug(f"name={__name__}")


def test_app_config_exists():
    logger.debug("test_app_config_exists()")
    cfg = app_config()
    assert cfg, "app_config is null"


def test_app_setting_exists():
    logger.debug("test_app_setting_exists()")
    o = app_settings()
    assert o, "app_settings is null"
