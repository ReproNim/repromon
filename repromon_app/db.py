import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from repromon_app.dao import BaseDAO

logger = logging.getLogger(__name__)
logger.debug(f"name={__name__}")


############################################
# DB engine

def db_init(params: dict, session_scopefunc=None):
    """ Initializes DB engine pool

    :param params: parameters dict, "url" is obligatory there
    :param session_scopefunc: optional session identity scope function
    :return:
    """
    logger.debug("db_init(...)")
    engine = create_engine(**params)
    logger.debug(f"created DB engine={str(engine)}")

    BaseDAO.default_session = scoped_session(
        sessionmaker(bind=engine), scopefunc=session_scopefunc
    )
    logger.debug("done")


def db_session_done():
    """ Terminates scoped session when execution context is destroyed

    :return:
    """
    logger.debug("db_session_done()")
    BaseDAO.default_session.remove()
