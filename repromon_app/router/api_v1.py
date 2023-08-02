import logging
from typing import Optional

from fastapi import (APIRouter, Query, Request, WebSocket, WebSocketDisconnect,
                     WebSocketException)

from repromon_app.model import (LoginInfoDTO, MessageLogInfoDTO,
                                PushMessageDTO, Rolename, StudyInfoDTO)
from repromon_app.security import security_check
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

    async def broadcast(self, msg: PushMessageDTO):
        logger.debug(f"broadcast(msg={str(msg.json())})")
        logger.debug(f"connections count: {len(self._connections)}")
        txt: str = msg.json()
        for conn in self._connections:
            await conn.send_text(txt)

    def remove(self, conn: WebSocket):
        logger.debug("remove(...)")
        self._connections.remove(conn)


def create_api_v1_router() -> APIRouter:
    api_v1_router = APIRouter()
    websocket_channel: WebsocketChannel = WebsocketChannel()
    PushService.channel = websocket_channel

    ##############################################
    # FeedbackService public API

    # @security: role=data_collector, auth
    @api_v1_router.get("/feedback/get_message",
                       response_model=MessageLogInfoDTO | None,
                       tags=["FeedbackService"],
                       summary="get_message",
                       description="Get single message log info by message ID")
    def feedback_get_message(request: Request,
                             message_id: int = Query(...,
                                                     description="Message ID")
                             ) -> MessageLogInfoDTO | None:
        logger.debug("feedback_get_message")
        security_check(rolename=Rolename.DATA_COLLECTOR)
        return FeedbackService().get_message(message_id)

    # @security: role=data_collector, auth
    @api_v1_router.get("/feedback/get_message_log",
                       response_model=list[MessageLogInfoDTO],
                       tags=["FeedbackService"],
                       summary="get_message_log",
                       description="Get study message log info")
    def feedback_get_message_log(request: Request,
                                 category_id: Optional[int] =
                                 Query(None,
                                       description="Category ID"),
                                 study_id: Optional[int] = Query(None,
                                                                 description="Study ID")
                                 ) -> list[MessageLogInfoDTO]:
        logger.debug("feedback_get_message_log")
        security_check(rolename=Rolename.DATA_COLLECTOR)
        return FeedbackService().get_message_log(category_id=category_id,
                                                 study_id=study_id)

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
        security_check(rolename=Rolename.DATA_COLLECTOR)
        return FeedbackService().get_study_header(study_id)

    # @security: role=data_collector, auth
    @api_v1_router.get("/feedback/set_message_log_visibility",
                       response_model=int,
                       tags=["FeedbackService"],
                       summary="set_message_log_visibility",
                       description="Update visibility for message log")
    def set_message_log_visibility(request: Request,
                                   category_id: int = Query(...,
                                                            description="Category ID"),
                                   visible: bool = Query(...,
                                                         description="Is row visible"),
                                   level: str = Query(...,
                                                      description="Level to update "
                                                                  "or * for any"),
                                   ) -> int:
        logger.debug("set_message_log_visibility")
        security_check(rolename=Rolename.DATA_COLLECTOR)
        return FeedbackService().set_message_log_visibility(category_id, visible, level)

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
        security_check(rolename=Rolename.ANY)
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
        except WebSocketDisconnect as wsd:
            logger.debug(f"websocket disconnect: {str(wsd)}")
        except WebSocketException as wse:
            logger.debug(f"websocket exception: {str(wse)}")
        finally:
            websocket_channel.remove(websocket)

    return api_v1_router
