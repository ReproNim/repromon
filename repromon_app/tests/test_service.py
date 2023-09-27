import logging

from repromon_app.dao import DAO
from repromon_app.model import (DataProviderId, MessageCategoryId,
                                MessageLevelId)
from repromon_app.service import (AccountService, FeedbackService,
                                  MessageService)

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


def test_account_get_roles():
    assert len(AccountService().get_roles()) > 0


def test_account_get_user():
    assert AccountService().get_user("tester1").username == "tester1"


def test_account_get_users():
    assert len(AccountService().get_users()) > 0


def test_feedback_get_devices():
    assert len(FeedbackService().get_devices()) > 0


def test_feedback_get_message():
    assert FeedbackService().get_message(-1) is None


def test_feedback_get_message_log():
    assert len(FeedbackService().get_message_log(None, None, None)) > 0


def test_feedback_get_study_header():
    assert FeedbackService().get_study_header(-1) is None


def test_message_send_message():
    msg = MessageService().send_message(
        "tester1", None, "Test Study Name",
        MessageCategoryId.FEEDBACK,
        MessageLevelId.INFO,
        1,
        DataProviderId.MRI,
        "Test message from test_service",
        "{'bar': 123}"
    )
    assert msg
    msg2 = DAO.message.get_message_log_info(msg.id)
    assert msg2
