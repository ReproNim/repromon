import contextvars
import logging
from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import (HTTPBasic, HTTPBasicCredentials,
                              OAuth2PasswordBearer)
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic.main import BaseModel

from repromon_app.config import app_settings
from repromon_app.dao import DAO
from repromon_app.model import Rolename, UserEntity, UserInfoDTO

logger = logging.getLogger(__name__)
logger.debug(f"name={__name__}")

############################################
# security things
# TODO: FastAPI move in some common web place
current_web_request = contextvars.ContextVar("current_web_request")


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
        self.__context_cache: dict = {}
        self.__user_cache: dict = {}
        self.__crypt_context: CryptContext = \
            CryptContext(schemes=["bcrypt"], deprecated="auto")

    def auth_user(self, username: str, password: str) -> bool:
        logger.debug(f"auth_user(username={username})")
        if not username:
            raise Exception("Invalid user name")

        user: UserEntity = None
        if username and username in self.__user_cache:
            user = self.__user_cache[username]
        else:
            user = DAO.account.get_user(username)
            if user:
                self.__user_cache[user.username] = user

        if not user:
            raise Exception(f"User not found: {username}")

        if user.is_active != 'Y':
            raise Exception(f"User is not active: {username}")

        if not self.verify_password(password, user.password):
            raise Exception("Invalid password")

        if user.username != username:
            raise Exception("Username mismatch")

        ctx = self.create_context_by_username(user.username)
        if not ctx:
            raise Exception("Auth internal error")

        return True

    def create_access_token(self, username: str, expire_sec: int = -1) -> str:
        logger.debug(f"create_access_token(username={username}, "
                     f"expire_sec={expire_sec})")
        if expire_sec <= 0:
            expire_sec = app_settings().TOKEN_EXPIRE_SEC
        if username and len(username) > 0:
            expire: datetime.datetime = \
                datetime.utcnow() + timedelta(seconds=expire_sec)
            data = {
                "sub": username,
                "exp": expire
            }
            logger.debug(f"data={str(data)}")
            token: str = jwt.encode(data,
                                    app_settings().TOKEN_SECRET_KEY,
                                    algorithm=app_settings().TOKEN_ALGORITHM
                                    )
            return token
        else:
            logger.error("Invalid user name")
            raise Exception("Invalid user name")

    def create_empty_context(self) -> SecurityContext:
        return SecurityContext(0, None, [], [])

    def create_context_by_username(self, username: str) -> SecurityContext:
        logger.debug(f"create_context_by_username(username={username})")
        if username and username in self.__context_cache:
            logger.debug(f"use cached security_context: {username}")
            return self.__context_cache[username]

        logger.debug("create new security_context")
        u: UserInfoDTO = DAO.account.get_user_info(username)
        if not u:
            raise Exception(
                f"Failed create security context. User not found: {username}"
            )
        roles: list[str] = DAO.sec_sys.get_rolename_by_username(username)
        devices: list[int] = DAO.sec_sys.get_device_id_by_username(username)
        ctx = SecurityContext(u.id, u.username, roles, devices)
        logger.debug(f"register security_context: {username}")
        self.__context_cache[username] = ctx
        return ctx

    def get_debug_context(self) -> SecurityContext:
        if not self.__debug_context:
            ctx: SecurityContext = None
            if app_settings().DEBUG_USERNAME:
                ctx = SecurityManager.instance().create_context_by_username(
                    app_settings().DEBUG_USERNAME
                )
                logger.debug(f"created debug context: {str(ctx)}")
            else:
                ctx = SecurityManager.instance().create_empty_context()

            self.__debug_context = ctx
            logger.debug(f"created debug context: {str(self.__debug_context)}")
        return self.__debug_context

    def get_context(self) -> SecurityContext:
        ctx: SecurityContext = None
        request = current_web_request.get()
        if request:
            ctx = getattr(request.state, "security_context", None)
            if ctx:
                return ctx

        ctx = self.get_debug_context()
        if ctx:
            if ctx.is_empty():
                logger.info("use empty context")
            return ctx

        logger.error("get_context not implemented")
        return None

    def get_password_hash(self, pwd: str) -> str:
        # return bcrypt.hash(pwd)
        return self.__crypt_context.hash(pwd)

    def get_username_by_token(self, token: str) -> str:
        logger.debug("get_username_by_token(...)")
        if token and len(token) > 0:
            try:
                data = jwt.decode(token,
                                  app_settings().TOKEN_SECRET_KEY,
                                  algorithms=[app_settings().TOKEN_ALGORITHM]
                                  )
                logger.debug(f"decoded data: {str(data)}")
                username: str = data.get("sub")
                if username:
                    return username
                raise Exception("Failed validate username credentials")
            except JWTError as e1:
                logger.error("Failed validate credentials", e1)
                raise Exception("Failed validate credentials")
        else:
            raise Exception("Not authenticated")

    def reset_cache(self, username: str = None):
        self.reset_context_cache(username)
        self.reset_user_cache(username)

    def reset_context_cache(self, username: str = None):
        logger.debug("reset_context_cache")
        if username:
            self.__context_cache.pop(username, None)
        else:
            self.__context_cache = {}

    def reset_user_cache(self, username: str = None):
        logger.debug("reset_user_cache")
        if username:
            self.__user_cache.pop(username, None)
        else:
            self.__user_cache = {}

    def verify_password(self, pwd: str, pwd_hash: str) -> bool:
        if pwd and pwd_hash:
            # return bcrypt.verify(pwd, pwd_hash)
            return self.__crypt_context.verify(pwd, pwd_hash)
        return False


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


############################################
# FastAPI security things
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)
basic_scheme = HTTPBasic()


class Token(BaseModel):
    access_token: str
    token_type: str


async def web_basic_context(
        request: Request,
        credentials: Annotated[HTTPBasicCredentials, Depends(basic_scheme)]
) -> SecurityContext:
    logger.debug("web_basic_context(...)")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Basic"},
    )
    try:
        mgr: SecurityManager = SecurityManager.instance()
        username: str = credentials.username
        logger.debug(f"username={username}")
        pwd: str = credentials.password
        if not mgr.auth_user(username, pwd):
            raise credentials_exception
        ctx: SecurityContext = mgr.create_context_by_username(username)
        request.state.security_context = ctx
        return ctx
    except BaseException as be:
        credentials_exception.detail = f"Unauthorized: {str(be)}"
        raise credentials_exception


async def _web_oauth2_context(
        request: Request,
        token: Annotated[str, Depends(oauth2_scheme)],
        strict: bool = True) -> SecurityContext:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unauthorized: Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    logger.debug(f"_web_oauth2_context, token: {token}, strict={strict}")
    try:
        mgr: SecurityManager = SecurityManager.instance()
        username: str = mgr.get_username_by_token(token)
        if username is None:
            if strict:
                raise credentials_exception
            return SecurityManager.instance().create_empty_context()
        ctx: SecurityContext = mgr.create_context_by_username(username)
        request.state.security_context = ctx
        return ctx
    except JWTError:
        if strict:
            raise credentials_exception
        return SecurityManager.instance().create_empty_context()
    except BaseException as be:
        if strict:
            credentials_exception.detail = f"Unauthorized: {str(be)}"
            raise credentials_exception
        return SecurityManager.instance().create_empty_context()


async def web_oauth2_context(
        request: Request,
        token: Annotated[str, Depends(oauth2_scheme)]) -> SecurityContext:
    return await _web_oauth2_context(request, token, strict=True)


async def web_oauth2_opt_context(
        request: Request,
        token: Annotated[str, Depends(oauth2_scheme)]) -> SecurityContext:
    return await _web_oauth2_context(request, token, strict=False)
