import logging
from repromon_app.dao import DAO
from repromon_app.model import RoleEntity, RoleInfoDTO, MessageLogInfoDTO, StudyInfoDTO, LoginInfoDTO, UserInfoDTO
from repromon_app.security import sec_ctx


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
        return self.dao.message_dao.get_message_log_infos(study_id)

    def get_study_header(self, study_id: int) -> StudyInfoDTO:
        logger.debug(f"get_study_header(study_id={str(study_id)})")
        return self.dao.study_dao.get_study_info(study_id)


# Login service, provides login/logout functionality
# and current login status
class LoginService(BaseService):
    def __init__(self):
        super().__init__()

    def get_current_user(self) -> LoginInfoDTO:
        li = LoginInfoDTO()
        li.username = sec_ctx().username
        li.is_logged_in = not(sec_ctx().is_empty())
        if li.is_logged_in:
            ui = self.dao.account.get_user_info(li.username)
            if ui:
                li.first_name = ui.first_name
                li.last_name = ui.last_name
        return li


# security system service to handle
# user, role permissions and similar
class SecSysService(BaseService):
    def __init__(self):
        super().__init__()

