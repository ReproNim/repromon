import asyncio
import logging
import uuid
from datetime import datetime

from repromon_app.dao import DAO
from repromon_app.model import (LoginInfoDTO, MessageLevel, MessageLogEntity,
                                MessageLogInfoDTO, MessagePayloadEntity,
                                PushMessageDTO, StudyDataEntity, StudyInfoDTO)
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


# service for feedback screen
class FeedbackService(BaseService):
    def __init__(self):
        super().__init__()

    def get_message(self, message_id: int) -> MessageLogInfoDTO:
        logger.debug(f"get_message(message_id={str(message_id)})")
        return self.dao.message.get_message_log_info(message_id)

    def get_message_log(self, study_id: int) -> list[MessageLogInfoDTO]:
        logger.debug(f"get_message_log(study_id={str(study_id)})")
        return self.dao.message.get_message_log_infos(study_id)

    def get_study_header(self, study_id: int) -> StudyInfoDTO:
        logger.debug(f"get_study_header(study_id={str(study_id)})")
        return self.dao.study.get_study_info(study_id)

    def set_message_log_visibility(self, study_id: int,
                                   visible: bool, level: str) -> int:
        logger.debug(f"set_message_log_visibility(study_id={str(study_id)},"
                     f" visible={visible}, level={level})")
        l: list[int] = [MessageLevel.ID_INFO,
                        MessageLevel.ID_WARN,
                        MessageLevel.ID_ERROR] \
            if level == MessageLevel.ANY else [MessageLevel.parse(level)]
        v: str = 'Y' if visible else 'N'
        res = self.dao.message.update_message_log_visibility(study_id, v, l)
        self.dao.message.commit()
        if res > 0:
            PushService().push_message("feedback-log-refresh", {"study_id": study_id})
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
            category_id: int,
            level_id: int,
            provider_id: int,
            description: str,
            payload: str,
    ) -> MessageLogEntity:
        logger.debug("send_message(...)")
        sd: StudyDataEntity = self.dao.study.get_study_data(study_id)

        p: MessagePayloadEntity = MessagePayloadEntity()
        p.uid = str(uuid.uuid4())
        p.payload = payload
        p.created_on = datetime.now()
        p.created_by = username

        self.dao.message.add(p)
        self.dao.message.flush()
        logger.debug(f"p={str(p)}")

        msg: MessageLogEntity = MessageLogEntity()
        msg.study_id = study_id
        msg.category_id = category_id
        msg.level_id = level_id
        msg.provider_id = provider_id
        msg.status_id = sd.status_id
        msg.is_visible = "Y"
        msg.description = description
        msg.payload_id = p.id
        msg.created_on = datetime.now()
        msg.created_by = username

        self.dao.message.add(msg)
        self.dao.message.commit()
        logger.debug(f"msg={str(msg)}")

        # send push notifications
        # NOTE: in future it should be published to message broker
        # rather than via PushService directly.
        PushService().push_message("feedback-log-add", {
            "study_id": msg.study_id,
            "message_id": msg.id}
        )
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
