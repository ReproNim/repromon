import logging

from repromon_app.config import app_settings
from repromon_app.dao import DAO
from repromon_app.model import Rolename, UserInfoDTO

logger = logging.getLogger(__name__)
logger.debug(f"name={__name__}")


############################################
# security things


# class representing current security context
class SecurityContext:
    def __init__(self, user_id: int, username: str,
                 rolenames: list[str], devices: list[int]):
        self.__user_id = user_id
        self.__username = username
        self.__rolenames = rolenames
        self.__devices = devices

    def is_empty(self) -> bool:
        return not (bool(self.__username))

    def has_device(self, device) -> bool:
        return True if device == '*' else int(device) in self.__devices

    def has_role(self, rolename: str) -> bool:
        return True if rolename == Rolename.ANY else rolename in self.__rolenames

    @property
    def devices(self) -> list[int]:
        return self.__devices

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
            f"username={self.__username}, "
            f"rolenames={str(self.__rolenames)}, "
            f"devices={str(self.__devices)})"
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
        return SecurityContext(0, None, [], [])

    def create_context_by_username(self, username: str) -> SecurityContext:
        logger.debug(f"create_context_by_username(username={username})")
        u: UserInfoDTO = DAO.account.get_user_info(username)
        if not u:
            raise Exception(
                f"Failed create security context. User not found: {username}"
            )
        roles: list[str] = DAO.sec_sys.get_rolename_by_username(username)
        devices: list[int] = DAO.sec_sys.get_device_id_by_username(username)
        ctx = SecurityContext(u.id, u.username, roles, devices)
        return ctx

    def get_debug_context(self) -> SecurityContext:
        if not self.__debug_context:
            ctx: SecurityContext = None
            if app_settings().DEBUG_USERNAME:
                ctx = SecurityManager().create_context_by_username(
                    app_settings().DEBUG_USERNAME
                )
                logger.debug(f"created debug context: {str(ctx)}")
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


# NOTE: in future can be extended with @security(rolename, device, ...) decorator
# to be applied around target method or function
def security_check(rolename=Rolename.ANY, device='*', env='*',
                   raise_exception: bool = True) -> list[str]:
    ctx: SecurityContext = security_context()
    errors: list[str] = []

    f_role: bool = any([ctx.has_role(r) for r in rolename]) \
        if isinstance(rolename, (list, tuple)) else ctx.has_role(rolename)

    if not f_role:
        logger.error(f"Security check, role mismatch: ctx={str(ctx)}, "
                     f"required rolename={str(rolename)}")
        errors.append("User role mismatch")

    f_device: bool = any([ctx.has_device(d) for d in device]) \
        if isinstance(device, (list, tuple)) else ctx.has_device(device)

    if not f_device:
        logger.error(f"Security check, device mismatch: ctx={str(ctx)}, "
                     f"required device={str(device)}")
        errors.append("User not allowed to work with this device")

    f_env: bool = app_settings().ENV in env if isinstance(env, (list, tuple)) \
        else env == app_settings().ENV or env == '*'

    if not f_env:
        logger.error(f"Security check, environment mismatch: ctx={str(ctx)}, "
                     f" required env={str(env)}")
        errors.append("Environment mismatch")

    if raise_exception and len(errors) > 0:
        raise Exception(f"Access denied. {'. '.join(errors)}")
    return errors
