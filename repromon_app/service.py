import asyncio
import logging
from datetime import datetime

from repromon_app.dao import DAO
from repromon_app.model import (DeviceEntity, LoginInfoDTO, MessageLevelId,
                                MessageLogEntity, MessageLogInfoDTO,
                                PushMessageDTO, RoleEntity, StudyDataEntity,
                                StudyInfoDTO, UserEntity)
from repromon_app.security import security_context

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
