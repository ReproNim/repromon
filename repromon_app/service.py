import logging
import uuid
from datetime import datetime
from repromon_app.dao import DAO
from repromon_app.model import RoleEntity, RoleInfoDTO, MessageLogInfoDTO, StudyInfoDTO, LoginInfoDTO, \
    UserInfoDTO, MessageLogEntity, MessagePayloadEntity, StudyDataEntity
from repromon_app.security import security_context


logger = logging.getLogger(__name__)
logger.debug("name=" + __name__)


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

    def get_message_log(self, study_id: int) -> list[MessageLogInfoDTO]:
        logger.debug(f"get_message_log(study_id={str(study_id)})")
        return self.dao.message.get_message_log_infos(study_id)

    def get_study_header(self, study_id: int) -> StudyInfoDTO:
        logger.debug(f"get_study_header(study_id={str(study_id)})")
        return self.dao.study.get_study_info(study_id)


# Login service, provides login/logout functionality
# and current login status
class LoginService(BaseService):
    def __init__(self):
        super().__init__()

    def get_current_user(self) -> LoginInfoDTO:
        li = LoginInfoDTO()
        li.username = security_context().username
        li.is_logged_in = not(security_context().is_empty())
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

    def send_message(self, username: str, study_id: int, category_id: int, level_id: int, provider_id: int,
                     description: str, payload: str) -> MessageLogEntity:
        logger.debug("send_message(...)")
        sd: StudyDataEntity = self.dao.study.get_study_data(study_id)

        p: MessagePayloadEntity = MessagePayloadEntity()
        p.uid = str(uuid.uuid4())
        p.payload = payload
        p.created_on = datetime.now()
        p.created_by = username

        self.dao.message.add(p)
        self.dao.message.flush()
        logger.debug("p="+str(p))

        msg: MessageLogEntity = MessageLogEntity()
        msg.study_id = study_id
        msg.category_id = category_id
        msg.level_id = level_id
        msg.provider_id = provider_id
        msg.status_id = sd.status_id
        msg.description = description
        msg.payload_id = p.id
        msg.created_on = datetime.now()
        msg.created_by = username

        self.dao.message.add(msg)
        self.dao.message.commit()
        logger.debug("msg="+str(msg))
        return msg


# security system service to handle
# user, role permissions and similar
class SecSysService(BaseService):
    def __init__(self):
        super().__init__()

