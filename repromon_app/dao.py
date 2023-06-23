import logging

logger = logging.getLogger(__name__)
logger.debug("name=" + __name__)


############################################
# DAO


class BaseDAO:
    """Base class for all DAO objects
    """
    default_session = None

    def __init__(self):
        pass

    def session(self):
        return BaseDAO.default_session


# DAO factory
class DAO:
    def __init__(self):
        pass








