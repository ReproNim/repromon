import logging

from repromon_app.config import app_settings
from repromon_app.dao import DAO
from repromon_app.model import UserInfoDTO

logger = logging.getLogger(__name__)
logger.debug(f"name={__name__}")


############################################
# security things


# class representing current security context
class SecurityContext:
    def __init__(self, user_id: int, username: str, rolenames: list[str]):
        self.__user_id = user_id
        self.__username = username
        self.__rolenames = rolenames

    def is_empty(self) -> bool:
        return not (bool(self.__username))

    @property
    def user_id(self) -> int:
        return self.__user_id

    @property
    def username(self) -> str:
        return self.__username

    @property
    def rolenames(self) -> list[str]:
        return self.__rolenames

    def __repr__(self):
        return (
            f"SecurityContext(user_id={self.__user_id}, "
            f"username={self.__username}, rolenames={str(self.__rolenames)})"
        )


class SecurityManager:
    __instance = None

    @classmethod
    def instance(cls):
        if not SecurityManager.__instance:
            SecurityManager.__instance = SecurityManager()
        return SecurityManager.__instance

    def __init__(self):
        self.__debug_context: SecurityContext = None

    def create_empty_context(self) -> SecurityContext:
        return SecurityContext(0, None, ())

    def create_context_by_username(self, username: str) -> SecurityContext:
        logger.debug(f"create_context_by_username(username={username})")
        u: UserInfoDTO = DAO.account.get_user_info(username)
        if not u:
            raise Exception(
                f"Failed create security context. User not found: {username}"
            )
        roles: list[str] = DAO.sec_sys.get_rolename_by_username(username)
        ctx = SecurityContext(u.id, u.username, roles)
        return ctx

    def get_debug_context(self) -> SecurityContext:
        if not self.__debug_context:
            ctx: SecurityContext = None
            if app_settings().DEBUG_USERNAME:
                ctx = SecurityManager().create_context_by_username(
                    app_settings().DEBUG_USERNAME
                )
            else:
                ctx = SecurityManager.create_empty_context()

            self.__debug_context = ctx
            logger.debug(f"created debug context: {str(self.__debug_context)}")
        return self.__debug_context

    def get_context(self) -> SecurityContext:
        ctx: SecurityContext = self.get_debug_context()
        if not ctx.is_empty():
            return ctx

        logger.error("get_context not implemented")
        return None


o = SecurityManager.instance()


def security_context() -> SecurityContext:
    return SecurityManager.instance().get_context()
