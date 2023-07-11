import logging

from fastapi import APIRouter, Query, Request, WebSocket

from repromon_app.model import (LoginInfoDTO, MessageLogInfoDTO,
                                PushMessageDTO, StudyInfoDTO)
from repromon_app.service import FeedbackService, LoginService, PushService

logger = logging.getLogger(__name__)
logger.debug(f"name={__name__}")


class WebsocketChannel:
    def __init__(self):
        self._connections: list[WebSocket] = []
        pass

    def add(self, conn: WebSocket):
        logger.debug("add(...)")
        self._connections.append(conn)

    def push(self, msg: PushMessageDTO):
        logger.debug("push(...)")
        logger.debug(f"connections count: {len(self._connections)}")
        txt: str = msg.json()
        for conn in self._connections:
            conn.send_text(txt)

    def remove(self, conn: WebSocket):
        logger.debug("remove(...)")
        self._connections.remove(conn)


def create_api_v1_router() -> APIRouter:
    api_v1_router = APIRouter()
    websocket_channel: WebsocketChannel = WebsocketChannel()
    PushService.websocket_channel = websocket_channel

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

    ##############################################
    # WebSocket public API
    @api_v1_router.websocket("/ws")
    async def ws(websocket: WebSocket):
        await websocket.accept()
        websocket_channel.add(websocket)
        try:
            while True:
                data = await websocket.receive_text()
                logger.debug(f"data={str(data)}")
                # await websocket.send_text(f"Message text was: {data}")
        finally:
            websocket_channel.remove(websocket)

    return api_v1_router
