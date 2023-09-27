import logging

from repromon_app.dao import DAO
from repromon_app.service import AccountService

logger = logging.getLogger(__name__)
logger.debug(f"name={__name__}")


def test_account_add_role():
    r = DAO.account.get_role_by_rolename("tester1")
    if r:
        DAO.account.delete(r)

    r = AccountService().add_role("tester1", "test role")
    assert r
    if r:
        DAO.account.delete(r)


def test_account_add_user():
    u = DAO.account.get_user("tester0")
    if u:
        DAO.account.delete(u)

    u = AccountService().add_user(
        "tester0", False, False,
        "Tester", "0", None, None, "Tester0 user"
    )
    assert u
    if u:
        DAO.account.delete(u)
