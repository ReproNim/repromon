import logging

from repromon_app.dao import DAO
from repromon_app.model import Rolename

logger = logging.getLogger(__name__)
logger.debug(f"name={__name__}")


def test_account_get_roles():
    logger.debug("test_account_get_roles()")
    assert len(DAO.account.get_roles()) > 0


def test_account_get_role_by_id():
    assert DAO.account.get_role_by_id(1)


def test_account_get_role_by_rolename():
    assert DAO.account.get_role_by_rolename(Rolename.DATA_COLLECTOR)


def test_account_get_role_infos():
    assert len(DAO.account.get_role_infos()) > 0


def test_account_get_user():
    assert DAO.account.get_user("tester1").username == "tester1"


def test_account_get_user_by_apikey():
    u = DAO.account.get_user("tester1")
    assert DAO.account.get_user_by_apikey(u.apikey).username == "tester1"


def test_account_get_users():
    assert len(DAO.account.get_users()) > 0


def test_account_get_user_info():
    assert DAO.account.get_user_info("tester1").username == "tester1"


def test_account_add_update_user():
    u = DAO.account.get_user("tester0")
    if u:
        DAO.account.delete(u)
        DAO.account.commit()

    assert DAO.account.get_user("tester0") is None
    assert DAO.account.add_user("tester0", "N", "N", "Tester", "0", None, None, None)
    u = DAO.account.get_user("tester0")
    assert u
    assert u.username == "tester0"

    u = DAO.account.get_user("tester0")
    if u:
        DAO.account.delete(u)
        DAO.account.commit()
