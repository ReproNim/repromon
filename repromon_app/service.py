import asyncio
import logging
from datetime import datetime

from repromon_app.config import app_settings
from repromon_app.dao import DAO
from repromon_app.model import (DeviceEntity, LoginInfoDTO, MessageLevelId,
                                MessageLogEntity, MessageLogInfoDTO,
                                PushMessageDTO, RoleEntity,
                                SecUserDeviceEntity, SecUserRoleEntity,
                                StudyDataEntity, StudyInfoDTO, UserEntity)
from repromon_app.security import (ApiKey, SecurityManager, Token,
                                   security_context)

logger = logging.getLogger(__name__)
logger.debug(f"name={__name__}")


############################################
# Services


# base class for all business services
class BaseService:
    def __init__(self):
        # TODO: make DAO singleton
        self.dao = DAO()


# service to handle account functionality
# user, role registration, login and onboarding
class AccountService(BaseService):
    def __init__(self):
        super().__init__()

    def add_role(self, rolename: str, description: str) -> RoleEntity:
        logger.debug(f"add_role(rolename={rolename},"
                     f" description={description})")
        return self.dao.account.add_role(rolename, description)

    def add_user(self, username: str, is_active: bool, is_system: bool,
                 first_name: str, last_name: str, email: str,
                 phone: str, description: str) -> UserEntity:
        logger.debug(f"add_user(username={username},"
                     f" is_active={is_active},"
                     f" is_system={is_system},"
                     f" first_name={first_name},"
                     f" last_name={last_name},"
                     f" email={email},"
                     f" phone={phone},"
                     f" description={description}"
                     f")"
                     )
        return self.dao.account.add_user(username,
                                         'Y' if is_active else 'N',
                                         'Y' if is_system else 'N',
                                         first_name,
                                         last_name,
                                         email,
                                         phone,
                                         description
                                         )

    def get_roles(self) -> list[RoleEntity]:
        logger.debug("get_roles()")
        return self.dao.account.get_roles()

    def get_user(self, username: str) -> UserEntity:
        logger.debug(f"get_user(username={username})")
        return self.dao.account.get_user(username)

    def get_users(self) -> list[UserEntity]:
        logger.debug("get_users()")
        return self.dao.account.get_users()


# service for feedback screen
class FeedbackService(BaseService):
    def __init__(self):
        super().__init__()

    def get_devices(self) -> list[DeviceEntity]:
        logger.debug("get_devices()")
        return self.dao.message.get_devices()

    def get_message(self, message_id: int) -> MessageLogInfoDTO:
        logger.debug(f"get_message(message_id={str(message_id)})")
        return self.dao.message.get_message_log_info(message_id)

    def get_message_log(self, category_id: int = None,
                        study_id: int = None,
                        interval_sec: int = None
                        ) -> list[MessageLogInfoDTO]:
        logger.debug(f"get_message_log(category_id={str(category_id)} "
                     f"study_id={str(study_id)})")
        return self.dao.message.get_message_log_infos(category_id,
                                                      study_id, interval_sec)

    def get_study_header(self, study_id: int) -> StudyInfoDTO:
        logger.debug(f"get_study_header(study_id={str(study_id)})")
        return self.dao.study.get_study_info(study_id)

    def set_message_log_visibility(self, category_id: int,
                                   visible: bool, level: str,
                                   interval_sec: int) -> int:
        logger.debug(f"set_message_log_visibility(category_id={str(category_id)},"
                     f" visible={visible}, level={level},"
                     f" interval_sec={interval_sec})")
        level_parsed: int = MessageLevelId.parse(level)
        l: list[int] = [MessageLevelId.INFO,
                        MessageLevelId.WARNING,
                        MessageLevelId.ERROR] \
            if level_parsed == MessageLevelId.ANY else [level_parsed]
        v: str = 'Y' if visible else 'N'
        res = self.dao.message.update_message_log_visibility(category_id, v, l,
                                                             interval_sec,
                                                             security_context().username)
        self.dao.message.commit()
        if res > 0:
            PushService().push_message("feedback-log-refresh",
                                       {"category_id": category_id})
        return res

    def set_message_log_visibility_by_ids(self,
                                          category_id: int,
                                          ids: list[int],
                                          visible: bool) -> int:
        logger.debug(f"set_message_log_visibility_ids(category_id={str(category_id)},"
                     f" ids={str(ids)},"
                     f" visible={visible})")
        v: str = 'Y' if visible else 'N'
        res = self.dao.message.update_message_log_visibility_by_ids(
            ids, v, security_context().username)
        self.dao.message.commit()
        if res > 0:
            if visible:
                PushService().push_message("feedback-log-refresh",
                                           {"category_id": category_id})
            else:
                PushService().push_message("feedback-log-delete",
                                           {
                                               "category_id": category_id,
                                               "message_ids": ids
                                           })
        return res


# Login service, provides login/logout functionality
# and current login status
class LoginService(BaseService):
    def __init__(self):
        super().__init__()

    def get_current_user(self) -> LoginInfoDTO:
        li = LoginInfoDTO()
        li.username = security_context().username
        li.is_logged_in = not (security_context().is_empty())
        if li.is_logged_in:
            ui = self.dao.account.get_user_info(li.username)
            if ui:
                li.first_name = ui.first_name
                li.last_name = ui.last_name
        return li


# service to handle messaging functionality
class MessageService(BaseService):
    def __init__(self):
        super().__init__()

    def send_message(
            self,
            username: str,
            study_id: int,
            study_name: str,
            category_id: int,
            level_id: int,
            device_id: int,
            provider_id: int,
            description: str,
            payload: str,
            event_on: datetime = None,
            registered_on: datetime = None
    ) -> MessageLogEntity:
        logger.debug("send_message(...)")
        sd: StudyDataEntity = self.dao.study.get_study_data(study_id) \
            if study_id else None

        msg: MessageLogEntity = MessageLogEntity()
        msg.study_id = study_id
        if sd:
            msg.study_name = sd.name
        if study_name:
            msg.study_name = study_name
        msg.category_id = category_id
        msg.level_id = level_id
        msg.provider_id = provider_id
        msg.is_visible = "Y"
        msg.description = description
        msg.payload = payload
        msg.event_on = event_on if event_on else datetime.now()
        msg.registered_on = registered_on if registered_on else datetime.now()
        msg.device_id = device_id
        msg.recorded_on = datetime.now()
        msg.recorded_by = username

        self.dao.message.add(msg)
        self.dao.message.commit()
        logger.debug(f"msg={str(msg)}")

        # send push notifications
        # NOTE: in future it should be published to message broker
        # rather than via PushService directly.
        PushService().push_message("feedback-log-add", {
            "category_id": category_id,
            "study_id": msg.study_id,
            "message_id": msg.id})
        return msg


# service to handle push messaging functionality in client-server web app
class PushService(BaseService):
    channel: object = None

    def push_message(self, topic: str, body: object):
        logger.debug(f"push_message(topic={topic}, body={str(body)})")
        if not PushService.channel:
            logger.error("PushService.channel is not initialized yet")
            return

        msg: PushMessageDTO = PushMessageDTO(
            topic=topic,
            ts=datetime.now(),
            sender=security_context().username,
            body=body)
        asyncio.run(PushService.channel.broadcast(msg))


# security system service to handle
# user, role permissions and similar
class SecSysService(BaseService):
    def __init__(self):
        super().__init__()

    def calculate_apikey(self, apikey_data: str) -> str:
        logger.debug(f"calculate_apikey(apikey_data={apikey_data})")
        apikey: ApiKey = SecurityManager.instance().calculate_apikey(apikey_data)
        return apikey.key

    def create_access_token(self, username: str,
                            expire_sec: int = 0) -> Token:
        logger.debug(f"create_access_token(username={username}, "
                     f"expire_sec={expire_sec})")
        if expire_sec <= 0:
            expire_sec = app_settings().TOKEN_EXPIRE_SEC
        logger.debug(f"expire_sec={expire_sec}")
        token: str = SecurityManager.instance().create_access_token(
            username, expire_sec)
        res: Token = Token(access_token=token, token_type="bearer")
        return res

    def create_apikey(self) -> ApiKey:
        logger.debug("create_apikey()")
        return SecurityManager.instance().create_apikey()

    def get_apikey_hash(self, apikey: str) -> str:
        logger.debug("get_apikey_hash(...)")
        return SecurityManager.instance().get_apikey_hash(apikey)

    def get_password_hash(self, pwd: str) -> str:
        logger.debug("get_password_hash(...)")
        return SecurityManager.instance().get_password_hash(pwd)

    def get_user_apikey(self, username: str) -> ApiKey:
        logger.debug(f"get_user_apikey(username={username})")
        return SecurityManager.instance().get_apikey_by_user(username)

    def get_user_devices(self, username: str) -> list[str]:
        logger.debug(f"get_user_devices(username={username})")
        return self.dao.sec_sys.get_device_id_by_username(username)

    def get_user_roles(self, username: str) -> list[str]:
        logger.debug(f"get_user_roles(username={username})")
        return self.dao.sec_sys.get_rolename_by_username(username)

    def get_users_by_role(self, rolename: str) -> list[str]:
        logger.debug(f"get_users_by_role(rolename={rolename})")
        return self.dao.sec_sys.get_username_by_rolename(rolename)

    def get_username_by_apikey(self, apikey: str) -> str:
        logger.debug("get_username_by_apikey(...)")
        return SecurityManager.instance().get_username_by_apikey(apikey)

    def get_username_by_token(self, token: str) -> str:
        logger.debug("get_username_by_token(...)")
        return SecurityManager.instance().get_username_by_token(token)

    def set_user_active(self, username: str,
                        is_active: bool) -> UserEntity:
        logger.debug(f"set_user_active(username={username}, "
                     f"is_active={is_active}...)")
        res: UserEntity = self.dao.account.update_user_is_active(
            username,
            'Y' if is_active else 'N')
        if res:
            SecurityManager.instance().reset_user_cache(username)
        return res

    def renew_user_apikey(self, username: str) -> ApiKey:
        logger.debug(f"renew_user_apikey(username={username})")
        apikey: ApiKey = SecurityManager.instance().create_apikey()
        apikey_hash: str = SecurityManager.instance().get_apikey_hash(apikey.key)
        u: UserEntity = self.dao.account.update_user_apikey(username,
                                                            apikey_hash,
                                                            apikey.data)
        SecurityManager.instance().reset_user_cache(u.username)
        return apikey

    def revoke_user_apikey(self, username: str):
        logger.debug(f"revoke_user_apikey(username={username})")
        u: UserEntity = self.dao.account.update_user_apikey(username,
                                                            None,
                                                            None)
        SecurityManager.instance().reset_user_cache(u.username)

    def set_user_password(self, username: str,
                          pwd: str) -> UserEntity:
        logger.debug(f"set_user_password(username={username}, ...)")
        pwd_hash: str = SecurityManager.instance().get_password_hash(pwd)
        res: UserEntity = self.dao.account.update_user_password(username, pwd_hash)
        if res:
            SecurityManager.instance().reset_user_cache(username)
        return res

    def set_user_devices(self, username: str,
                         devices: list[str]) -> list[str]:
        logger.debug(f"set_user_devices(username={username}, "
                     f"devices={devices})")
        user: UserEntity = self.dao.account.get_user(username)
        if not user:
            raise Exception("User not found")

        # get devices cache
        devices_all: list[DeviceEntity] = self.dao.message.get_devices()
        map_name = {str(d.id): d for d in devices_all} | \
                   {d.kind: d for d in devices_all} | \
                   {d.description: d for d in devices_all}
        map_id = {d.id: d for d in devices_all}

        # get list of device IDs to be set for user
        set1: set[int] = {map_name[s].id for s in devices if s in map_name}

        lst: SecUserDeviceEntity = self.dao.sec_sys.get_sec_user_device_by_user_id(
            user.id)
        map_entity = {e.device_id: e for e in lst}

        # get list of device IDs user already have
        set2: set[int] = set(de.device_id for de in lst)

        # calculate list device IDs to be added in sec_user_device
        set_to_add: set[int] = set1 - set2
        logger.debug(f"set_to_add={set_to_add}")

        # calculate list device IDs to be removed from sec_user_device
        set_to_del: set[int] = set2 - set1
        logger.debug(f"set_to_del={set_to_del}")

        # calculate list device IDs to be returned
        set_to_res: set[int] = set1 & set2
        logger.debug(f"set_to_res={set_to_res}")

        for id_del in set_to_del:
            logger.debug(f"delete device with id={id_del}")
            self.dao.sec_sys.delete_sec_user_device_by_id(map_entity[id_del].id)

        for id_add in set_to_add:
            logger.debug(f"add device with id={id_add}")
            self.dao.sec_sys.add_sec_user_device(user.id, id_add)

        # reset security context cache for the user
        SecurityManager.instance().reset_context_cache(username)

        return list(str(map_id[id_res].id) for id_res in set_to_res)

    def set_user_roles(self, username: str,
                       rolenames: list[str]) -> list[str]:
        logger.debug(f"set_user_roles(username={username}, "
                     f"rolenames={rolenames})")
        user: UserEntity = self.dao.account.get_user(username)
        if not user:
            raise Exception("User not found")

        # get all roles cache
        roles_all: list[RoleEntity] = self.dao.account.get_roles()
        map_name = {r.rolename: r for r in roles_all} | \
                   {str(r.id): r for r in roles_all} | \
                   {r.description: r for r in roles_all}
        map_id = {r.id: r for r in roles_all}

        # get list of role IDs to be set for user
        set1: set[int] = {map_name[s].id for s in rolenames if s in map_name}

        lst: SecUserRoleEntity = self.dao.sec_sys.get_sec_user_role_by_user_id(
            user.id)
        map_entity = {e.role_id: e for e in lst}

        # get list of role IDs user already have
        set2: set[int] = set(re.role_id for re in lst)

        # calculate list role IDs to be added in sec_user_role
        set_to_add: set[int] = set1 - set2
        logger.debug(f"set_to_add={set_to_add}")

        # calculate list role IDs to be removed from sec_user_role
        set_to_del: set[int] = set2 - set1
        logger.debug(f"set_to_del={set_to_del}")

        # calculate list role IDs to be returned
        set_to_res: set[int] = set1 & set2
        logger.debug(f"set_to_res={set_to_res}")

        for id_del in set_to_del:
            logger.debug(f"delete role with id={id_del}")
            self.dao.sec_sys.delete_sec_user_role_by_id(map_entity[id_del].id)

        for id_add in set_to_add:
            logger.debug(f"add role with id={id_add}")
            self.dao.sec_sys.add_sec_user_role(user.id, id_add)

        # reset security context cache for the user
        SecurityManager.instance().reset_context_cache(username)

        return list(map_id[id_res].rolename for id_res in set_to_res)
