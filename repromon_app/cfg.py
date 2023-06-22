import logging
import pydantic
import configparser
import platform
from pathlib import Path
import sys
import time


logger = logging.getLogger(__name__)


class FlaskCfg(pydantic.BaseModel):
    """ Flask configuration under [FLASK] section
    """
    FLASK_ENV: str = None
    DEBUG: bool = False
    MAX_CONTENT_LENGTH: str = "@| int(1000000)"
    MAX_COOKIE_SIZE: str = "@|int(4096)"
    SERVER_NAME: str = "127.0.0.1:5050"
    APPLICATION_ROOT: str = "/repromon"
    PREFERRED_URL_SCHEME: str = None
    EXPLAIN_TEMPLATE_LOADING: str = None
    TEMPLATES_AUTO_RELOAD: str = None


class RepromonCfg(pydantic.BaseModel):
    """ Basic configuration for [REPROMON] section
    """
    ENV: str = "Unknown"


class AppCfg:
    """Application configuration
    """
    instance = None

    #
    LOGGING_INI = "logging.ini"
    APP_INI = "repromon.ini"
    #
    SECTION_SYSTEM = "SYSTEM"
    SECTION_REPROMON = "REPROMON"
    SECTION_FLASK = "FLASK"

    # AppConfig members
    def __init__(self):
        self.ROOT_PATH = str(Path(__file__).parent.parent)
        self.HOST_CONFIG_PATH = "/etc/repronim/repromon"
        self.START_TIME = time.time()
        self.CONFIG_PATH = None
        self.REPROMON: RepromonCfg = RepromonCfg()
        self.FLASK: FlaskCfg = FlaskCfg()

    def to_dict(self):
        return {
            "ROOT_PATH": self.ROOT_PATH,
            "HOST_CONFIG_PATH": self.HOST_CONFIG_PATH,
            "START_TIME": self.START_TIME,
            "CONFIG_PATH": self.CONFIG_PATH,
            "REPROMON": self.REPROMON.dict(),
            "FLASK": self.FLASK.dict()
        }


def app_cfg() -> AppCfg:
    """Get application configuration

    :return: Current application configuration
    """
    return AppCfg.instance


def app_cfg_init() -> None:
    """Initializes logger and application configuration from INI file
    and environment variables
    """
    logger.debug("app_cfg_init()")

    if AppCfg.instance:
        logger.info("Application config already initialized")
        return

    cfg = AppCfg()
    AppCfg.instance = cfg

    # init logger
    log_files = [
        cfg.HOST_CONFIG_PATH + '/' + AppCfg.LOGGING_INI,
        cfg.ROOT_PATH + '/' + AppCfg.LOGGING_INI
    ]

    for log_file in log_files:
        if Path(log_file).exists():
            logging.config.fileConfig(log_file, disable_existing_loggers=False)
            logger.info("Found logger configuration file: "+str(log_file))
            break

    logger.info("Application configuration init...")
    logger.info('[Platform Info]: ')
    logger.info(' system    : ' + platform.system())
    logger.info(' node      : ' + platform.node())
    logger.info(' release   : ' + platform.release())
    logger.info(' version   : ' + platform.version())
    logger.info(' machine   : ' + platform.machine())
    logger.info(' processor : ' + platform.processor())
    logger.info(' python    : ' + '.'.join(map(str, sys.version_info)) + ', ' + sys.executable)

    # load configuration from multiple INI files
    ini_paths = [
        cfg.ROOT_PATH + '/' + AppCfg.APP_INI,
        cfg.HOST_CONFIG_PATH + '/' + AppCfg.APP_INI
    ]

    for ini_path in ini_paths:
        if Path(ini_path).exists():
            logging.config.fileConfig(log_file, disable_existing_loggers=False)
            logger.info("Found ini configuration file: "+str(ini_path))

            cp = configparser.ConfigParser()
            # keep property names as is
            cp.optionxform = str
            with open(ini_path) as fd:
                cp.read_file(fd)

            cfg.REPROMON = RepromonCfg(**cp[AppCfg.SECTION_REPROMON])
            cfg.FLASK = FlaskCfg(**cp[AppCfg.SECTION_FLASK])

            break

    logger.info('Environment: '+cfg.REPROMON.ENV)
    logger.info("Application config initialized successfully")
    #logger.debug(cfg.to_dict())

