import logging
import os
import platform
import sys
import time
from configparser import ConfigParser, ExtendedInterpolation
from pathlib import Path
from typing import Optional

import pydantic
from dotenv import dotenv_values

logger = logging.getLogger(__name__)


class BaseSectionConfig(pydantic.BaseModel):
    """Base class for section configuration"""

    pass


class DbConfig(BaseSectionConfig):
    """Database configuration under [db***] sections for SQLAlchemy"""

    url: str = None
    arg_schema: str = None
    echo: bool = False
    pool_size: int = 5
    pool_recycle: int = 3600


class SettingsConfig(BaseSectionConfig):
    """Basic configuration for [system] section"""

    ENV: str = "local"
    CORS_ALLOW_ORIGINS: str = None
    DEBUG_USERNAME: str = None
    APIKEY_SECRET: str = None
    APIKEY_SALT: str = "1"
    INITIAL_ADMIN_PASSWORD: str = None
    TOKEN_SECRET_KEY: str = None
    TOKEN_ALGORITHM: str = "HS256"
    TOKEN_EXPIRE_SEC: int = 24 * 60 * 60
    UI_APP_PATH: str = None
    UI2_APP_PATH: str = None
    WEB_HOST: str = "localhost"
    WEB_PORT: int = 9095

    @property
    def CORS_ALLOW_ORIGINS_LIST(self) -> list[str]:
        if self.CORS_ALLOW_ORIGINS:
            return self.CORS_ALLOW_ORIGINS.splitlines()
        else:
            return []


class UvicornConfig(BaseSectionConfig):
    """Basic configuration for [uvicorn] section"""
    host: Optional[str] = "127.0.0.1"
    port: Optional[int] = 5050
    # workers: Optional[int] = None
    # reload: Optional[bool] = False
    # log_level: Optional[str] = "info"
    # access_log: Optional[bool] = True
    # timeout_keep_alive: Optional[int] = 5
    # limit_concurrency: Optional[int] = 100
    # limit_max_requests: Optional[int] = 0
    ssl_keyfile: Optional[str] = None
    ssl_certfile: Optional[str] = None


class AppConfig:
    """Application configuration"""

    instance = None

    #
    LOGGING_INI = "logging.ini"
    APP_INI = "repromon.ini"
    #
    SECTION_SETTINGS = "settings"
    SECTION_UVICORN = "uvicorn"
    SECTION_DB = "db"

    # AppConfig members
    def __init__(self):
        self.ROOT_PATH = str(Path(__file__).parent.parent)
        self.WEBCONTENT_PATH = f"{self.ROOT_PATH}/repromon_app/webcontent"
        self.HOST_CONFIG_PATH = "/etc/repronim/repromon"
        self.START_TIME = time.time()
        self.CONFIG_PATH = None
        self.settings: SettingsConfig = SettingsConfig()
        self.uvicorn: UvicornConfig = UvicornConfig()
        self.db: DbConfig = DbConfig()

    def to_dict(self):
        return {
            "ROOT_PATH": self.ROOT_PATH,
            "WEBCONTENT_PATH": self.WEBCONTENT_PATH,
            "HOST_CONFIG_PATH": self.HOST_CONFIG_PATH,
            "START_TIME": self.START_TIME,
            "CONFIG_PATH": self.CONFIG_PATH,
            "[settings]": self.settings.dict(),
            "[db]": self.db.dict(),
            "[uvicorn]": self.uvicorn.dict(),
        }


class MacroExpander(ExtendedInterpolation):
    """Expand macros values with ${} pattern in configparser"""

    def __init__(self, params: dict):
        self._params = params

    def before_get(self, parser, section, option, value, defaults):
        # logger.debug(f"before_get() value={str(value)},"
        #              f" type={str(type(value))}")
        if value and value.find("$") >= 0:
            for k, v in self._params.items():
                value = value.replace("${" + k + "}", v)
                value = value.replace("{@ROOT_PATH}", self._params["ROOT_PATH"])
        return super().before_get(parser, section, option, value, defaults)


def app_config() -> AppConfig:
    """Get application configuration

    :return: Current application configuration
    """
    return AppConfig.instance


def app_config_init() -> None:
    """Initializes logger and application configuration from INI file
    and environment variables
    """
    logger.debug("app_cfg_init()")

    if AppConfig.instance:
        logger.info("Application config already initialized")
        return

    cfg = AppConfig()
    AppConfig.instance = cfg

    # init logger
    log_files = [
        f"{cfg.HOST_CONFIG_PATH}/{AppConfig.LOGGING_INI}",
        f"{cfg.ROOT_PATH}/{AppConfig.LOGGING_INI}",
    ]

    for log_file in log_files:
        if Path(log_file).exists():
            if hasattr(logging, 'config'):
                logging.config.fileConfig(log_file, disable_existing_loggers=False)
            else:
                logger.error("logging.config not found, undefined")
                sys.stderr.write("!!! logging.config not found, undefined !!!\n")
            logger.info(f"Found logger configuration file: {str(log_file)}")
            break

    logger.info("Application configuration init...")
    logger.info("[Platform Info]: ")
    logger.info(f" system    : {platform.system()}")
    logger.info(f" node      : {platform.node()}")
    logger.info(f" release   : {platform.release()}")
    logger.info(f" version   : {platform.version()}")
    logger.info(f" machine   : {platform.machine()}")
    logger.info(f" processor : {platform.processor()}")
    logger.info(f" python    : {'.'.join(map(str, sys.version_info))},"
                f" {sys.executable}")

    # load configuration from multiple INI files
    ini_paths = [
        f"{cfg.ROOT_PATH}/{AppConfig.APP_INI}",
        f"{cfg.HOST_CONFIG_PATH}/{AppConfig.APP_INI}",
    ]

    default_env_path = f"{cfg.ROOT_PATH}/.env.local"

    for ini_path in ini_paths:
        if Path(ini_path).exists():
            # logging.config.fileConfig(log_file, disable_existing_loggers=False)
            logger.info(f"Found ini config file: {str(ini_path)}")

            params: dict = {}

            if Path(default_env_path).exists():
                logger.info(f"Found default env file: {str(default_env_path)}")
                params.update(dotenv_values(default_env_path))

            params.update(dict(os.environ))
            params.update({
                "ROOT_PATH": cfg.ROOT_PATH
            })

            cp = ConfigParser(interpolation=MacroExpander(params))
            # keep property names as is
            cp.optionxform = str
            with open(ini_path) as fd:
                cp.read_file(fd)

            cfg.settings = SettingsConfig(**cp[AppConfig.SECTION_SETTINGS])
            cfg.uvicorn = UvicornConfig(**cp[AppConfig.SECTION_UVICORN])
            cfg.db = DbConfig(**cp[AppConfig.SECTION_DB])

            break

    logger.info(f"Environment: {cfg.settings.ENV}")
    logger.info("Application config initialized successfully")
    # logger.debug(json.dumps(cfg.to_dict(), indent=4))


def app_settings() -> SettingsConfig:
    """Get application settings configuration

    :return: Current application settings configuration
    """
    return app_config().settings
