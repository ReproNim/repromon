import logging
from datetime import datetime
from typing import Annotated, Optional

from fastapi import (APIRouter, Depends, Query, Request, WebSocket,
                     WebSocketDisconnect, WebSocketException)

from repromon_app.model import (ApiKeyInfoDTO, DataProviderId, DeviceEntity,
                                LoginInfoDTO, MessageCategoryId,
                                MessageLevelId, MessageLogEntity,
                                MessageLogInfoDTO, PushMessageDTO, RoleEntity,
                                Rolename, StudyInfoDTO, UserEntity)
from repromon_app.security import (ApiKey, SecurityContext, SecurityManager,
                                   Token, security_check, security_context,
                                   web_oauth2_apikey_context,
                                   web_oauth2_context, web_oauth2_opt_context)
from repromon_app.service import (AccountService, FeedbackService,
                                  LoginService, MessageService, PushService,
                                  SecSysService)

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
    # AccountService public API

    # @security: admin
    @api_v1_router.get("/account/add_user",
                       response_model=object,
                       tags=["AccountService"],
                       summary="add_user",
                       description="Register new user in system")
    def account_add_user(request: Request,
                         sec_ctx:
                         Annotated[SecurityContext, Depends(web_oauth2_context)],
                         username: str =
                         Query(...,
                               description="Unique username"),
                         is_active: bool =
                         Query(...,
                               description="Specify if user is active"),
                         is_system: bool =
                         Query(...,
                               description="Specify if user is system one"),
                         first_name: str =
                         Query(...,
                               description="User first name"),
                         last_name: str =
                         Query(...,
                               description="User last name"),
                         email: Optional[str] =
                         Query(None,
                               description="User e-mail"),
                         phone: Optional[str] =
                         Query(None,
                               description="User phone"),
                         description: Optional[str] =
                         Query(None,
                               description="User account description"),
                         ) -> UserEntity:
        logger.debug(f"account_add_user(username={username})")
        security_check(rolename=Rolename.ADMIN)
        svc: AccountService = AccountService()
        o: UserEntity = svc.add_user(
            username,
            is_active,
            is_system,
            first_name,
            last_name,
            email,
            phone,
            description
        )
        return o.copy().clean_sensitive_info() if o else None

    # @security: admin
    @api_v1_router.get("/account/get_roles",
                       response_model=list,
                       tags=["AccountService"],
                       summary="get_roles",
                       description="Get all roles")
    def account_get_roles(request: Request,
                          sec_ctx:
                          Annotated[SecurityContext, Depends(web_oauth2_context)],
                          ) -> list[RoleEntity]:
        logger.debug("account_get_roles")
        security_check(rolename=Rolename.ADMIN)
        return AccountService().get_roles()

    # @security: admin
    @api_v1_router.get("/account/get_user",
                       response_model=object,
                       tags=["AccountService"],
                       summary="get_user",
                       description="Get user by username")
    def account_get_user(request: Request,
                         sec_ctx:
                         Annotated[SecurityContext, Depends(web_oauth2_context)],
                         username: str = Query(...,
                                               description="Username"),
                         ) -> UserEntity:
        logger.debug(f"account_get_user(username={username})")
        security_check(rolename=Rolename.ADMIN)
        o: UserEntity = AccountService().get_user(username)
        return o.clean_sensitive_info() if o else None

    # @security: admin
    @api_v1_router.get("/account/get_users",
                       response_model=list,
                       tags=["AccountService"],
                       summary="get_users",
                       description="Get all users")
    def account_get_users(request: Request,
                          sec_ctx:
                          Annotated[SecurityContext, Depends(web_oauth2_context)],
                          ) -> list[UserEntity]:
        logger.debug("account_get_users")
        security_check(rolename=Rolename.ADMIN)
        users: list[UserEntity] = [user.copy().clean_sensitive_info()
                                   for user in AccountService().get_users()]
        return users

    ##############################################
    # FeedbackService public API

    # @security: role=data_collector, auth
    @api_v1_router.get("/feedback/get_devices",
                       response_model=list,
                       tags=["FeedbackService"],
                       summary="get_devices",
                       description="Get DeviceEntity device list")
    def feedback_get_devices(request: Request,
                             sec_ctx:
                             Annotated[SecurityContext, Depends(
                                 web_oauth2_context)]) -> list[DeviceEntity]:
        logger.debug("feedback_get_devices()")
        security_check(rolename=[Rolename.DATA_COLLECTOR, Rolename.ADMIN])
        return FeedbackService().get_devices()

    # @security: role=data_collector, auth
    @api_v1_router.get("/feedback/get_message",
                       response_model=MessageLogInfoDTO | None,
                       tags=["FeedbackService"],
                       summary="get_message",
                       description="Get single message log info by message ID")
    def feedback_get_message(request: Request,
                             sec_ctx:
                             Annotated[SecurityContext, Depends(
                                 web_oauth2_context)],
                             message_id: int = Query(...,
                                                     description="Message ID")
                             ) -> MessageLogInfoDTO | None:
        logger.debug("feedback_get_message")
        security_check(rolename=[Rolename.ADMIN, Rolename.DATA_COLLECTOR])
        return FeedbackService().get_message(message_id)

    # @security: role=data_collector, auth
    @api_v1_router.get("/feedback/get_message_log",
                       response_model=list[MessageLogInfoDTO],
                       tags=["FeedbackService"],
                       summary="get_message_log",
                       description="Get study message log info")
    def feedback_get_message_log(request: Request,
                                 sec_ctx:
                                 Annotated[SecurityContext, Depends(
                                     web_oauth2_context)],
                                 category_id: Optional[int] =
                                 Query(None,
                                       description="Category ID"),
                                 study_id: Optional[int] = Query(None,
                                                                 description="Study ID"),
                                 interval_sec: Optional[int] =
                                 Query(None,
                                       description="Interval in "
                                                   "seconds for latest messages"),
                                 ) -> list[MessageLogInfoDTO]:
        logger.debug("feedback_get_message_log")
        security_check(rolename=[Rolename.ADMIN, Rolename.DATA_COLLECTOR])
        return FeedbackService().get_message_log(category_id=category_id,
                                                 study_id=study_id,
                                                 interval_sec=interval_sec)

    # @security: role=data_collector, auth
    @api_v1_router.get("/feedback/get_study_header",
                       response_model=StudyInfoDTO | None,
                       tags=["FeedbackService"],
                       summary="get_study_header",
                       description="Get study header info")
    def feedback_get_study_header(request: Request,
                                  sec_ctx:
                                  Annotated[SecurityContext, Depends(
                                      web_oauth2_context)],
                                  study_id: int = Query(...,
                                                        description="Study ID")
                                  ) -> StudyInfoDTO:
        logger.debug("feedback_get_study_header")
        security_check(rolename=[Rolename.ADMIN, Rolename.DATA_COLLECTOR])
        return FeedbackService().get_study_header(study_id)

    # @security: role=data_collector, auth
    @api_v1_router.get("/feedback/set_message_log_visibility",
                       response_model=int,
                       tags=["FeedbackService"],
                       summary="set_message_log_visibility",
                       description="Update visibility for message log")
    def set_message_log_visibility(request: Request,
                                   sec_ctx:
                                   Annotated[SecurityContext, Depends(
                                       web_oauth2_context)],
                                   category_id: int = Query(...,
                                                            description="Category ID"),
                                   visible: bool = Query(...,
                                                         description="Is row visible"),
                                   level: str = Query(...,
                                                      description="Level to update "
                                                                  "or * for any"),
                                   interval_sec: Optional[int] =
                                   Query(None,
                                         description="Interval in "
                                                     "seconds for latest messages"),
                                   ) -> int:
        logger.debug("set_message_log_visibility")
        security_check(rolename=[Rolename.ADMIN, Rolename.DATA_COLLECTOR])
        return FeedbackService().set_message_log_visibility(category_id,
                                                            visible, level,
                                                            interval_sec)

    # @security: role=data_collector, auth
    @api_v1_router.get("/feedback/set_message_log_visibility_by_ids",
                       response_model=int,
                       tags=["FeedbackService"],
                       summary="set_message_log_visibility_by_ids",
                       description="Update visibility for message log by message IDs")
    def set_message_log_visibility_by_ids(request: Request,
                                          sec_ctx:
                                          Annotated[SecurityContext, Depends(
                                              web_oauth2_context)],
                                          category_id: int =
                                          Query(...,
                                                description="Category ID"),
                                          message_ids: list[int] =
                                          Query(...,
                                                description="Message ID list"),
                                          visible: bool =
                                          Query(...,
                                                description="Is row visible"),
                                          ) -> int:
        logger.debug("set_message_log_visibility_by_ids")
        security_check(rolename=[Rolename.ADMIN, Rolename.DATA_COLLECTOR])
        return FeedbackService().set_message_log_visibility_by_ids(category_id,
                                                                   message_ids,
                                                                   visible)

    ##############################################
    # LoginService public API

    # @security: any
    @api_v1_router.get("/login/get_current_user",
                       response_model=LoginInfoDTO,
                       tags=["LoginService"],
                       summary="get_current_user",
                       description="Get current user info")
    def login_get_current_user(request: Request,
                               sec_ctx:
                               Annotated[SecurityContext, Depends(
                                   web_oauth2_opt_context)],
                               ) -> LoginInfoDTO:
        logger.debug("login_get_current_user")
        security_check(rolename=Rolename.ANY)
        return LoginService().get_current_user()

    ##############################################
    # MessageService public API

    # @security: admin | sys_data_entry
    @api_v1_router.post("/message/send_message",
                        response_model=MessageLogInfoDTO,
                        tags=["MessageService"],
                        summary="send_message",
                        description="Send ReproMon message")
    def send_message(request: Request,
                     sec_ctx: Annotated[SecurityContext, Depends(
                         web_oauth2_apikey_context)],
                     study: Optional[str] = Query(None,
                                                  description="Study name or ID if any"),
                     category: str = Query(...,
                                           description="Category name or ID, "
                                                       "e.g. Feedback | 1"),
                     level: str = Query(...,
                                        description="Message level, int ID or  "
                                                    "level name, "
                                                    "e.g ERROR | WARNING | INFO"),

                     device: Optional[str] = Query(None,
                                                   description="Device ID if any, "
                                                               "e.g. MRI or 1"),
                     provider: str = Query(...,
                                           description="Provider name or ID, "
                                                       "e.g. ReproIn | ReproStim | "
                                                       "ReproEvents | PACS | "
                                                       "Noisseur | DICOM/QA | "
                                                       "MRI etc"),
                     description: str = Query(...,
                                              description="Message description"),
                     payload: Optional[str] = Query(None,
                                                    description="Message JSON"
                                                                " payload if any"),
                     event_on: Optional[datetime] =
                     Query(None,
                           description="Timestamp "
                                       "of the event in the "
                                       "ISO 8601 format like "
                                       "YYYY-MM-DDTHH:MM:SS"
                                       ".ssssss"),
                     registered_on: Optional[datetime] =
                     Query(None,
                           description="Timestamp of "
                                       "registration in the ISO 8601 format like "
                                       "YYYY-MM-DDTHH:MM:SS.ssssss"),
                     ) -> MessageLogInfoDTO:
        logger.debug("send_message")
        security_check(rolename=[Rolename.ADMIN, Rolename.SYS_DATA_ENTRY])
        o: MessageLogEntity = MessageService().send_message(
            security_context().username,
            None,
            study,
            MessageCategoryId.parse(category),
            MessageLevelId.parse(level),
            1,  # TODO: device ID
            DataProviderId.parse(provider),
            description,
            payload,
            event_on,
            registered_on
        )
        logger.debug(f"id={o.id}")
        res: MessageLogInfoDTO = FeedbackService().get_message(o.id)
        return res

    ##############################################
    # SecSysService public API

    # @security: admin
    @api_v1_router.get("/secsys/calculate_apikey",
                       response_model=str,
                       tags=["SecSysService"],
                       summary="calculate_apikey",
                       description="Calculate API key from apikey_data")
    def secsys_calculate_apikey(request: Request,
                                sec_ctx:
                                Annotated[SecurityContext, Depends(
                                    web_oauth2_context)],
                                apikey_data: str =
                                Query(...,
                                      description="API key data"),
                                ) -> str:
        logger.debug(f"secsys_calculate_apikey(apikey_data={apikey_data})")
        security_check(rolename=Rolename.ADMIN)
        svc: SecSysService = SecSysService()
        return svc.calculate_apikey(apikey_data)

    # @security: admin
    @api_v1_router.get("/secsys/create_access_token",
                       response_model=Token,
                       tags=["SecSysService"],
                       summary="create_access_token",
                       description="Create OAuth2+JWT token with "
                                   "custom expiration time")
    def secsys_create_access_token(request: Request,
                                   sec_ctx:
                                   Annotated[SecurityContext, Depends(
                                       web_oauth2_context)],
                                   username: str =
                                   Query(...,
                                         description="Specify username"),
                                   expire_sec: int =
                                   Query(...,
                                         description="Token expiration time in seconds. "
                                                     "To set default expiration time "
                                                     "set value to 0 or negative"),
                                   ) -> Token:
        logger.debug(f"secsys_create_access_token(username={username}, "
                     f"expire_sec={expire_sec})")
        security_check(rolename=Rolename.ADMIN)
        svc: SecSysService = SecSysService()
        return svc.create_access_token(username, expire_sec)

    # @security: admin
    @api_v1_router.get("/secsys/create_apikey",
                       response_model=ApiKey,
                       tags=["SecSysService"],
                       summary="create_apikey",
                       description="Create generic API key")
    def secsys_create_apikey(request: Request,
                             sec_ctx:
                             Annotated[SecurityContext, Depends(
                                 web_oauth2_context)],
                             ) -> str:
        logger.debug("secsys_create_apikey()")
        security_check(rolename=Rolename.ADMIN)
        svc: SecSysService = SecSysService()
        return svc.create_apikey()

    # @security: admin
    @api_v1_router.get("/secsys/get_all_apikeys",
                       response_model=list[ApiKeyInfoDTO],
                       tags=["SecSysService"],
                       summary="get_all_apikeys",
                       description="Get all API keys as list")
    def secsys_get_all_apikeys(request: Request,
                               sec_ctx:
                               Annotated[SecurityContext, Depends(web_oauth2_context)],
                               ) -> list[ApiKeyInfoDTO]:
        logger.debug("secsys_get_all_apikeys()")
        security_check(rolename=Rolename.ADMIN)
        svc: SecSysService = SecSysService()
        return svc.get_all_apikeys()

    # @security: admin
    @api_v1_router.get("/secsys/get_apikey_hash",
                       response_model=object,
                       tags=["SecSysService"],
                       summary="get_apikey_hash",
                       description="Generate API key hash from API key string")
    def secsys_get_apikey_hash(request: Request,
                               sec_ctx:
                               Annotated[SecurityContext, Depends(
                                   web_oauth2_context)],
                               apikey: str =
                               Query(...,
                                     description="API key value"),
                               ) -> object:
        logger.debug("secsys_get_apikey_hash(...)")
        security_check(rolename=Rolename.ADMIN)
        svc: SecSysService = SecSysService()
        return {"apikey_hash": svc.get_apikey_hash(apikey)}

    # @security: admin
    @api_v1_router.get("/secsys/get_password_hash",
                       response_model=object,
                       tags=["SecSysService"],
                       summary="get_password_hash",
                       description="Generate password hash from password string")
    def secsys_get_password_hash(request: Request,
                                 sec_ctx:
                                 Annotated[SecurityContext, Depends(
                                     web_oauth2_context)],
                                 password: str =
                                 Query(...,
                                       description="Password value"),
                                 ) -> object:
        logger.debug("secsys_get_password_hash(...)")
        security_check(rolename=Rolename.ADMIN)
        svc: SecSysService = SecSysService()
        return {"password_hash": svc.get_password_hash(password)}

    # @security: admin
    @api_v1_router.get("/secsys/get_user_apikey",
                       response_model=ApiKeyInfoDTO,
                       tags=["SecSysService"],
                       summary="get_user_apikey",
                       description="Get user current API key if any")
    def secsys_get_user_apikey(request: Request,
                               sec_ctx:
                               Annotated[SecurityContext, Depends(web_oauth2_context)],
                               username: str =
                               Query(...,
                                     description="Specify username"),
                               ) -> ApiKeyInfoDTO:
        logger.debug(f"secsys_get_user_apikey(username={username})")
        security_check(rolename=Rolename.ADMIN)
        svc: SecSysService = SecSysService()
        return svc.get_user_apikey(username)

    # @security: admin
    @api_v1_router.get("/secsys/get_user_devices",
                       response_model=list,
                       tags=["SecSysService"],
                       summary="get_user_devices",
                       description="Get devices user has access to")
    def secsys_get_user_devices(request: Request,
                                sec_ctx:
                                Annotated[SecurityContext, Depends(web_oauth2_context)],
                                username: str =
                                Query(...,
                                      description="Specify username"),
                                ) -> UserEntity:
        logger.debug(f"secsys_get_user_devices(username={username})")
        security_check(rolename=Rolename.ADMIN)
        svc: SecSysService = SecSysService()
        return svc.get_user_devices(username)

    # @security: admin
    @api_v1_router.get("/secsys/get_user_roles",
                       response_model=list,
                       tags=["SecSysService"],
                       summary="get_user_roles",
                       description="Get rolename list user has access to")
    def secsys_get_user_roles(request: Request,
                              sec_ctx:
                              Annotated[SecurityContext, Depends(web_oauth2_context)],
                              username: str =
                              Query(...,
                                    description="Specify username"),
                              ) -> UserEntity:
        logger.debug(f"secsys_get_user_roles(username={username})")
        security_check(rolename=Rolename.ADMIN)
        svc: SecSysService = SecSysService()
        return svc.get_user_roles(username)

    # @security: admin
    @api_v1_router.get("/secsys/get_users_by_role",
                       response_model=list,
                       tags=["SecSysService"],
                       summary="get_users_by_role",
                       description="Get all users with specified rolename")
    def secsys_get_users_by_role(request: Request,
                                 sec_ctx:
                                 Annotated[SecurityContext, Depends(web_oauth2_context)],
                                 rolename: str =
                                 Query(...,
                                       description="Specify rolename"),
                                 ) -> UserEntity:
        logger.debug(f"secsys_get_users_by_role(rolename={rolename})")
        security_check(rolename=Rolename.ADMIN)
        svc: SecSysService = SecSysService()
        return svc.get_users_by_role(rolename)

    # @security: admin
    @api_v1_router.get("/secsys/get_username_by_apikey",
                       response_model=object,
                       tags=["SecSysService"],
                       summary="get_username_by_apikey",
                       description="Retrieve username from API key")
    def secsys_get_username_by_apikey(request: Request,
                                      sec_ctx:
                                      Annotated[SecurityContext, Depends(
                                          web_oauth2_context)],
                                      apikey: str =
                                      Query(...,
                                            description="API key value"),
                                      ) -> object:
        logger.debug("secsys_get_username_by_apikey(...)")
        security_check(rolename=Rolename.ADMIN)
        svc: SecSysService = SecSysService()
        return {"username": svc.get_username_by_apikey(apikey)}

    # @security: admin
    @api_v1_router.get("/secsys/get_username_by_token",
                       response_model=object,
                       tags=["SecSysService"],
                       summary="get_username_by_token",
                       description="Extract username from access token")
    def secsys_get_username_by_token(request: Request,
                                     sec_ctx:
                                     Annotated[SecurityContext, Depends(
                                         web_oauth2_context)],
                                     token: str =
                                     Query(...,
                                           description="Access token value"),
                                     ) -> object:
        logger.debug("secsys_get_username_by_token(...)")
        security_check(rolename=Rolename.ADMIN)
        svc: SecSysService = SecSysService()
        return {"username": svc.get_username_by_token(token)}

    # @security: admin
    @api_v1_router.get("/secsys/renew_user_apikey",
                       response_model=object,
                       tags=["SecSysService"],
                       summary="renew_user_apikey",
                       description="Renew API key for the specified user")
    def secsys_renew_user_apikey(request: Request,
                                 sec_ctx:
                                 Annotated[SecurityContext, Depends(web_oauth2_context)],
                                 username: str =
                                 Query(...,
                                       description="Specify username"),
                                 ) -> UserEntity:
        logger.debug(f"secsys_renew_user_apikey(username={username})")
        security_check(rolename=Rolename.ADMIN)
        svc: SecSysService = SecSysService()
        ak: ApiKey = svc.renew_user_apikey(username)
        return {"username": username, "apikey": ak.key}

    # @security: admin
    @api_v1_router.get("/secsys/revoke_user_apikey",
                       response_model=object,
                       tags=["SecSysService"],
                       summary="revoke_user_apikey",
                       description="Remove API key for the specified user")
    def secsys_revoke_user_apikey(request: Request,
                                  sec_ctx:
                                  Annotated[SecurityContext, Depends(
                                      web_oauth2_context)],
                                  username: str =
                                  Query(...,
                                        description="Specify username"),
                                  ) -> UserEntity:
        logger.debug(f"secsys_revoke_user_apikey(username={username})")
        security_check(rolename=Rolename.ADMIN)
        svc: SecSysService = SecSysService()
        svc.revoke_user_apikey(username)
        return {"detail": f"API key revoked for {username}"}

    # @security: admin
    @api_v1_router.get("/secsys/set_user_active",
                       response_model=object,
                       tags=["SecSysService"],
                       summary="set_user_active",
                       description="Update user activity status")
    def secsys_set_user_active(request: Request,
                               sec_ctx:
                               Annotated[SecurityContext, Depends(web_oauth2_context)],
                               username: str =
                               Query(...,
                                     description="Specify username"),
                               is_active: bool =
                               Query(...,
                                     description="Specify user activity "
                                                 "status to be set"),
                               ) -> UserEntity:
        logger.debug(f"secsys_set_user_active(username={username}, "
                     f"is_active={is_active})")
        security_check(rolename=Rolename.ADMIN)
        svc: SecSysService = SecSysService()
        o: UserEntity = svc.set_user_active(username, is_active)
        return o.copy().clean_sensitive_info() if o else None

    # @security: admin
    @api_v1_router.get("/secsys/set_user_password",
                       response_model=object,
                       tags=["SecSysService"],
                       summary="set_user_password",
                       description="Set user account password")
    def secsys_set_user_password(request: Request,
                                 sec_ctx:
                                 Annotated[SecurityContext, Depends(web_oauth2_context)],
                                 username: str =
                                 Query(...,
                                       description="Specify username"),
                                 password: str =
                                 Query(...,
                                       description="New user password to be set"),
                                 ) -> UserEntity:
        logger.debug(f"secsys_set_user_password(username={username})")
        security_check(rolename=Rolename.ADMIN)
        svc: SecSysService = SecSysService()
        o: UserEntity = svc.set_user_password(username, password)
        return o.copy().clean_sensitive_info() if o else None

    # @security: admin
    @api_v1_router.get("/secsys/set_user_devices",
                       response_model=object,
                       tags=["SecSysService"],
                       summary="set_user_devices",
                       description="Set user devices")
    def secsys_set_user_devices(request: Request,
                                sec_ctx:
                                Annotated[SecurityContext, Depends(web_oauth2_context)],
                                username: str =
                                Query(...,
                                      description="Specify username"),
                                devices: Optional[list[str]] =
                                Query([],
                                      description="Specify list of all user devices "
                                                  "(device ID, device kind or "
                                                  "device description)"),
                                ) -> object:
        logger.debug(f"secsys_set_user_devices(username={username} "
                     f"devices={devices})")
        security_check(rolename=Rolename.ADMIN)
        svc: SecSysService = SecSysService()
        devices_before: list[str] = svc.get_user_devices(username)
        svc.set_user_devices(username, devices)
        devices_after: list[str] = svc.get_user_devices(username)
        return {
            "username": username,
            "devices_before": devices_before,
            "devices_after": devices_after
        }

    # @security: admin
    @api_v1_router.get("/secsys/set_user_roles",
                       response_model=object,
                       tags=["SecSysService"],
                       summary="set_user_roles",
                       description="Set user roles")
    def secsys_set_user_roles(request: Request,
                              sec_ctx:
                              Annotated[SecurityContext, Depends(web_oauth2_context)],
                              username: str =
                              Query(...,
                                    description="Specify username"),
                              rolenames: Optional[list[str]] =
                              Query([],
                                    description="Specify list of all user roles "
                                                "(rolename, role ID or role "
                                                "description)"),
                              ) -> object:
        logger.debug(f"secsys_set_user_devices(username={username} "
                     f"rolenames={rolenames})")
        security_check(rolename=Rolename.ADMIN)
        svc: SecSysService = SecSysService()
        roles_before: list[str] = svc.get_user_roles(username)
        svc.set_user_roles(username, rolenames)
        roles_after: list[str] = svc.get_user_roles(username)
        return {
            "username": username,
            "roles_before": roles_before,
            "roles_after": roles_after
        }

    ##############################################
    # WebSocket public API
    @api_v1_router.websocket("/ws")
    async def ws(websocket: WebSocket):
        await websocket.accept()
        f_registered: bool = False
        try:
            logger.debug(f"waiting for access token to be sent: {str(websocket)}")
            token: str = await websocket.receive_text()
            if not SecurityManager.instance().verify_token(token):
                await websocket.close(code=4000, reason="Invalid access token")
                return

            websocket_channel.add(websocket)
            logger.debug(f"register new authenticated connection: {str(websocket)}")
            f_registered = True

            while True:
                data = await websocket.receive_text()
                logger.debug(f"data={str(data)}")
                # await websocket.send_text(f"Message text was: {data}")
        except WebSocketDisconnect as wsd:
            logger.debug(f"websocket disconnect: {str(wsd)}")
        except WebSocketException as wse:
            logger.debug(f"websocket exception: {str(wse)}")
        finally:
            if f_registered:
                websocket_channel.remove(websocket)

    return api_v1_router
