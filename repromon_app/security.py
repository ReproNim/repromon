import base64
import contextvars
import hashlib
import logging
import uuid
from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import (APIKeyHeader, HTTPBasic, HTTPBasicCredentials,
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


class ApiKey(BaseModel):
    key: str
    prefix: str
    body: str
    data: str


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
        self.__apikey_cache: dict = {}
        self.__crypt_pwd_context: CryptContext = \
            CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.__crypt_apikey_context: CryptContext = \
            CryptContext(schemes=["sha256_crypt"], deprecated="auto")

    def auth_user(self, username: str, password: str) -> bool:
        logger.debug(f"auth_user(username={username})")
        if not username:
            raise Exception("Invalid user name")

        user: UserEntity = self._get_cached_user(username)

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

    def calculate_apikey(self, apikey_data: str) -> ApiKey:
        logger.debug(f"calculate_apikey(apikey_data={apikey_data})")

        if not apikey_data:
            raise Exception("Empty apikey_data provided")

        if len(apikey_data) < 16:
            raise Exception("Too short apikey_data, should be at least 16 characters")

        # add secret to data
        src: str = f"{apikey_data}{app_settings().APIKEY_SECRET}"

        # take only last 43 chars from hash, use
        # predefined salt and rounds values
        body: str = self.__crypt_apikey_context.hash(
            src, salt=app_settings().APIKEY_SALT, rounds=1001)[-43:]

        # keep only [0-9a-zA-Z] characters
        body = ''.join(c for c in body if c.isalnum() or c.isdigit())

        # generate prefix, at this moment first 5 chars from apikey_data UID
        prefix: str = str(apikey_data)[0:5]

        # create key as prefix.body
        key = f"{prefix}.{body}"
        # logger.debug(f"key={key}")
        return ApiKey(key=key, prefix=prefix, body=body, data=apikey_data)

    def create_apikey(self) -> ApiKey:
        logger.debug("create_apikey()")

        apikey_data: str = str(uuid.uuid4())
        logger.debug(f"apikey_data={apikey_data}")

        apikey: str = self.calculate_apikey(apikey_data)
        return apikey

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

    def get_apikey_by_user(self, username: str) -> ApiKey:
        u: UserEntity = self._get_cached_user(username)

        if not u:
            raise Exception(f"User not found: {username}")

        if not u.apikey_data:
            raise Exception("User doesn't have API key")

        if len(u.apikey_data) < 16:
            raise Exception("User doesn't have valid API key")

        return self.calculate_apikey(u.apikey_data)

    def get_apikey_hash(self, apikey: str) -> str:
        if not apikey:
            raise Exception("Empty API key")

        a = apikey.split(".")
        if len(a) == 2:
            prefix: str = a[0]

            # we use faster hash than for password in this case
            sha = hashlib.sha256()
            sha.update(apikey.encode('utf-8'))
            val = base64.b64encode(sha.digest()).decode('utf-8')
            return f"{str(prefix)}_{str(val)}"
        else:
            raise Exception("Invalid API key format")

    def _get_cached_user(self, username: str) -> UserEntity:
        user: UserEntity = None
        if username and username in self.__user_cache:
            user = self.__user_cache[username]
        else:
            user = DAO.account.get_user(username)
            if user:
                self.__user_cache[user.username] = user
        return user

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
        return self.__crypt_pwd_context.hash(pwd)

    def get_username_by_apikey(self, apikey: str) -> str:
        if apikey and apikey in self.__apikey_cache:
            username: str = self.__apikey_cache[apikey]
            if username and len(username) > 0:
                logger.debug(f"use cached apikey value for user: {username}")
                return username
            else:
                logger.debug("use cached apikey value for user: Invalid API key")
                raise Exception("Invalid API key")

        try:
            res: str = self.get_username_by_apikey_internal(apikey)
            self.__apikey_cache[apikey] = res
            return res
        except BaseException as e:
            self.__apikey_cache[apikey] = ""
            raise e

    def get_username_by_apikey_internal(self, apikey: str) -> str:
        logger.debug("get_username_by_apikey_internal(...)")
        if apikey and len(apikey) > 0:
            apikey_hash: str = self.get_apikey_hash(apikey)
            u: UserEntity = DAO.account.get_user_by_apikey(apikey_hash)
            if not u:
                raise Exception("Invalid API key")
            return u.username
        else:
            raise Exception("Invalid API key")

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
        self.reset_apikey_cache(username)

    def reset_apikey_cache(self, username: str = None):
        logger.debug("reset_apikey_cache")
        if username:
            keys = [k for k, v in self.__apikey_cache.items() if v == username]
            for key in keys:
                del self.__apikey_cache[key]
        else:
            self.__apikey_cache = {}

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

    def verify_token(self, token: str) -> bool:
        try:
            username: str = self.get_username_by_token(token)
            return False if username is None else True
        except JWTError as je:
            logger.error(f"Failed verify_token jwt, {str(je)}")
            return False
        except BaseException as be:
            logger.error(f"Failed verify_token, {str(be)}")
            return False

    def verify_password(self, pwd: str, pwd_hash: str) -> bool:
        if pwd and pwd_hash:
            # return bcrypt.verify(pwd, pwd_hash)
            return self.__crypt_pwd_context.verify(pwd, pwd_hash)
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
apikey_scheme = APIKeyHeader(name="X-API-Key", auto_error=False)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)
basic_scheme = HTTPBasic()


class Token(BaseModel):
    access_token: str
    token_type: str


async def web_apikey_context(
        request: Request,
        apikey: Annotated[str, Depends(apikey_scheme)]
) -> SecurityContext:
    logger.debug("web_apikey_context(...)")
    if not apikey:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authenticated"
        )
    try:
        mgr: SecurityManager = SecurityManager.instance()
        username: str = mgr.get_username_by_apikey(apikey)
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized: Could not validate API key"
            )
        ctx: SecurityContext = mgr.create_context_by_username(username)
        request.state.security_context = ctx
        return ctx
    except BaseException as be:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Unauthorized: {str(be)}"
        )


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


async def web_oauth2_apikey_context(
        request: Request,
        token: Annotated[str, Depends(oauth2_scheme)],
        apikey: Annotated[str, Depends(apikey_scheme)]) -> SecurityContext:
    if token:
        return await web_oauth2_context(request, token)
    else:
        return await web_apikey_context(request, apikey)
