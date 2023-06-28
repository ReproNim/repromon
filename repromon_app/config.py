import logging
import platform
import sys
import time
from configparser import ConfigParser, ExtendedInterpolation
from pathlib import Path

import pydantic

logger = logging.getLogger(__name__)


class BaseSectionConfig(pydantic.BaseModel):
    """Base class for section configuration"""

    pass


class DbConfig(BaseSectionConfig):
    """Flask configuration under [db***] sections for SQLAlchemy"""

    url: str = None
    echo: bool = False
    pool_size: int = 5
    pool_recycle: int = 3600


class FlaskConfig(BaseSectionConfig):
    """Flask configuration under [flask] section"""

    FLASK_ENV: str = None
    DEBUG: bool = False
    MAX_CONTENT_LENGTH: int = 1000000
    MAX_COOKIE_SIZE: int = 4096
    SERVER_NAME: str = "127.0.0.1:5050"
    APPLICATION_ROOT: str = "/repromon"
    PREFERRED_URL_SCHEME: str = None
    EXPLAIN_TEMPLATE_LOADING: str = None
    TEMPLATES_AUTO_RELOAD: str = None


class SettingsConfig(BaseSectionConfig):
    """Basic configuration for [system] section"""

    ENV: str = "Unknown"
    DEBUG_USERNAME: str = None


class AppConfig:
    """Application configuration"""

    instance = None

    #
    LOGGING_INI = "logging.ini"
    APP_INI = "repromon.ini"
    #
    SECTION_SETTINGS = "settings"
    SECTION_FLASK = "flask"
    SECTION_DB = "db"

    # AppConfig members
    def __init__(self):
        self.ROOT_PATH = str(Path(__file__).parent.parent)
        self.HOST_CONFIG_PATH = "/etc/repronim/repromon"
        self.START_TIME = time.time()
        self.CONFIG_PATH = None
        self.settings: SettingsConfig = SettingsConfig()
        self.flask: FlaskConfig = FlaskConfig()
        self.db: DbConfig = DbConfig()

    def to_dict(self):
        return {
            "ROOT_PATH": self.ROOT_PATH,
            "HOST_CONFIG_PATH": self.HOST_CONFIG_PATH,
            "START_TIME": self.START_TIME,
            "CONFIG_PATH": self.CONFIG_PATH,
            "[settings]": self.settings.dict(),
            "[db]": self.db.dict(),
            "[flask]": self.flask.dict(),
        }


class MacroExpander(ExtendedInterpolation):
    """Expand macros values with ${} pattern in configparser"""

    def __init__(self, params: dict):
        self._params = params

    def before_get(self, parser, section, option, value, defaults):
        logger.debug(f"before_get() value={str(value)},"
                     f" type={str(type(value))}")
        if value and value.find("$") >= 0:
            for k, v in self._params.items():
                value = value.replace("${" + k + "}", v)
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
        cfg.HOST_CONFIG_PATH + "/" + AppConfig.LOGGING_INI,
        cfg.ROOT_PATH + "/" + AppConfig.LOGGING_INI,
    ]

    for log_file in log_files:
        if Path(log_file).exists():
            logging.config.fileConfig(log_file, disable_existing_loggers=False)
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
        cfg.ROOT_PATH + "/" + AppConfig.APP_INI,
        cfg.HOST_CONFIG_PATH + "/" + AppConfig.APP_INI,
    ]

    for ini_path in ini_paths:
        if Path(ini_path).exists():
            logging.config.fileConfig(log_file, disable_existing_loggers=False)
            logger.info(f"Found ini config file: {str(ini_path)}")

            cp = ConfigParser(interpolation=MacroExpander(
                {"ROOT_PATH": cfg.ROOT_PATH}
            ))
            # keep property names as is
            cp.optionxform = str
            with open(ini_path) as fd:
                cp.read_file(fd)

            cfg.settings = SettingsConfig(**cp[AppConfig.SECTION_SETTINGS])
            cfg.flask = FlaskConfig(**cp[AppConfig.SECTION_FLASK])
            cfg.db = DbConfig(**cp[AppConfig.SECTION_DB])

            break

    logger.info("Environment: " + cfg.settings.ENV)
    logger.info("Application config initialized successfully")
    # logger.debug(json.dumps(cfg.to_dict(), indent=4))


def app_settings() -> SettingsConfig:
    """Get application settings configuration

    :return: Current application settings configuration
    """
    return app_config().settings
