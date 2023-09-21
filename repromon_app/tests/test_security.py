import logging

import pytest

from repromon_app.security import SecurityManager

logger = logging.getLogger(__name__)
logger.debug(f"name={__name__}")


def test_security_manager_exists():
    logger.debug("test_security_manager_exists")
    assert SecurityManager.instance(), "security manager not found"


@pytest.mark.parametrize(
    "pwd",
    [
        ("password321"),
        ("aaa"),
    ]
)
def test_get_password_hash(pwd):
    logger.debug(f"test_get_password_hash({pwd})")
    s = SecurityManager.instance().get_password_hash(pwd)
    logger.debug(f"hash={s}")
    assert len(s) > 0


@pytest.mark.parametrize(
    "pwd, pwd_hash",
    [
        ("password321", "$2b$12$iyRORLxvhqvPXT0yW/MarOnYxkc3QxA5Qy6Wh53AzB9hgZZGxZA.2"),
        ("aaa", "$2b$12$efrsbXTnd3lfansk9gs1XOpmAN3tczxDmn2a3AtUGomyIsXl5mr4O"),
    ]
)
def test_verify_password(pwd, pwd_hash):
    logger.debug(f"test_verify_password({pwd}, {pwd_hash})")
    assert SecurityManager.instance().verify_password(pwd, pwd_hash)
