import logging
from repromon_app.model import Rolename

logger = logging.getLogger(__name__)
logger.debug("name=" + __name__)

############################################
# security things


# class representing current security context
class SecurityContext:
    def __init__(self, user_id: int, username: str, rolenames: list[str]):
        self.__user_id = user_id
        self.__username = username
        self.__rolenames = rolenames

    def is_empty(self) -> bool:
        return not(bool(self.__username))

    @property
    def user_id(self) -> int:
        return self.__user_id

    @property
    def username(self) -> str:
        return self.__username

    @property
    def rolenames(self) -> list[str]:
        return self.__rolenames


class SecurityManager:
    def __init__(self):
        pass

    def create_empty_context(self):
        return SecurityContext(0, None, ())

    def create_shadowed_context(self):
        return SecurityContext(1, "user1", (Rolename.DATA_COLLECTOR))


TODO_current_sec_ctx = SecurityManager().create_shadowed_context()


def sec_ctx() -> SecurityContext:
    return TODO_current_sec_ctx
