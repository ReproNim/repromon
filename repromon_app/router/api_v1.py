import logging

from fastapi import APIRouter, Query, Request

from repromon_app.model import LoginInfoDTO, MessageLogInfoDTO, StudyInfoDTO
from repromon_app.service import FeedbackService, LoginService

logger = logging.getLogger(__name__)
logger.debug(f"name={__name__}")


def create_api_v1_router() -> APIRouter:
    api_v1_router = APIRouter()

    ##############################################
    # FeedbackService public API

    # @security: role=data_collector, auth
    @api_v1_router.get("/feedback/get_message_log",
                       response_model=list[MessageLogInfoDTO],
                       tags=["FeedbackService"],
                       summary="get_message_log",
                       description="Get study message log info")
    def feedback_get_message_log(request: Request,
                                 study_id: int = Query(...,
                                                       description="Study ID")
                                 ) -> list[MessageLogInfoDTO]:
        logger.debug("feedback_get_message_log")
        return FeedbackService().get_message_log(study_id)

    # @security: role=data_collector, auth
    @api_v1_router.get("/feedback/get_study_header",
                       response_model=StudyInfoDTO,
                       tags=["FeedbackService"],
                       summary="get_study_header",
                       description="Get study header info")
    def feedback_get_study_header(request: Request,
                                  study_id: int = Query(...,
                                                        description="Study ID")
                                  ) -> StudyInfoDTO:
        logger.debug("feedback_get_study_header")
        return FeedbackService().get_study_header(study_id)

    # @security: role=data_collector, auth
    @api_v1_router.get("/feedback/set_message_log_visibility",
                       response_model=int,
                       tags=["FeedbackService"],
                       summary="set_message_log_visibility",
                       description="Update visibility for message log")
    def set_message_log_visibility(request: Request,
                                   study_id: int = Query(...,
                                                         description="Study ID"),
                                   visible: bool = Query(...,
                                                         description="Is row visible"),
                                   level: str = Query(...,
                                                      description="Level to update "
                                                                  "or * for any"),
                                   ) -> int:
        logger.debug("set_message_log_visibility")
        return FeedbackService().set_message_log_visibility(study_id, visible, level)

    ##############################################
    # LoginService public API

    # @security: any
    @api_v1_router.get("/login/get_current_user",
                       response_model=LoginInfoDTO,
                       tags=["LoginService"],
                       summary="get_current_user",
                       description="Get current user info")
    def login_get_current_user(request: Request) -> LoginInfoDTO:
        logger.debug("login_get_current_user")
        return LoginService().get_current_user()

    return api_v1_router
