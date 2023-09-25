import logging

from repromon_app.dao import DAO, BaseDAO
from repromon_app.db import db_session_done

logger = logging.getLogger(__name__)
logger.debug(f"name={__name__}")


def test_db_initialized(
        apikey_tester1,
        apikey_tester2,
        apikey_tester3
):
    logger.debug("test_db_initialized()")
    assert BaseDAO.default_session, "session is null"
    assert DAO.account.session(), "session() is null"
    assert apikey_tester1 and len(apikey_tester1) > 0
    assert apikey_tester2 and len(apikey_tester2) > 0
    assert apikey_tester3 and len(apikey_tester3) > 0
    db_session_done()
