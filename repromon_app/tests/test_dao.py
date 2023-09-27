import logging

from repromon_app.dao import DAO
from repromon_app.model import MessageCategoryId, Rolename

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

    DAO.account.update_user_apikey("tester0", "apikey0", "data0")
    DAO.account.update_user_password("tester0", "password0")
    DAO.account.update_user_is_active("tester0", "N")

    u = DAO.account.get_user("tester0")
    assert u.apikey == "apikey0"
    assert u.apikey_data == "data0"
    assert u.password == "password0"
    assert u.is_active == 'N'

    if u:
        DAO.account.delete(u)
        DAO.account.commit()


def test_message_get_data_providers():
    assert len(DAO.message.get_data_providers()) > 0


def test_message_get_devices():
    assert len(DAO.message.get_devices()) > 0


def test_message_get_message_levels():
    assert len(DAO.message.get_message_levels()) > 0


def test_message_get_message_log_infos():
    lst = DAO.message.get_message_log_infos(MessageCategoryId.FEEDBACK, None, None)
    assert len(lst) > 0
    msg0 = lst[0]
    assert DAO.message.get_message_log_info(msg0.id)


def test_sec_sys_get_device_id_by_username():
    assert len(DAO.sec_sys.get_device_id_by_username("tester1")) > 0


def test_sec_sys_get_sec_user_device_by_user_id():
    user_id = DAO.account.get_user("tester1").id
    assert len(DAO.sec_sys.get_sec_user_device_by_user_id(user_id)) > 0


def test_sec_sys_get_sec_user_role_by_user_id():
    user_id = DAO.account.get_user("tester1").id
    assert len(DAO.sec_sys.get_sec_user_role_by_user_id(user_id)) > 0


def test_sec_sys_get_username_by_rolename():
    assert len(DAO.sec_sys.get_username_by_rolename(Rolename.ADMIN)) > 0


def test_sec_sys_get_rolename_by_username():
    assert len(DAO.sec_sys.get_rolename_by_username("tester1")) > 0


def test_study_get_study_data():
    assert DAO.study.get_study_data(-1) is None


def test_study_get_study_info():
    assert DAO.study.get_study_info(-1) is None
