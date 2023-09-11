import json
import logging
from typing import Annotated

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from repromon_app.config import app_config, app_settings
from repromon_app.dao import DAO
from repromon_app.model import MessageCategoryId, MessageLogEntity, Rolename
from repromon_app.security import (SecurityContext, Token, security_check,
                                   security_context, web_basic_context)
from repromon_app.service import MessageService, SecSysService

logger = logging.getLogger(__name__)
logger.debug(f"name={__name__}")


def create_admin_router() -> APIRouter:
    admin_router = APIRouter()
    admin_router.mount("/static",
                       StaticFiles(
                           directory=f"{app_config().WEBCONTENT_PATH}/static"
                       ),
                       name="static")
    _templates = Jinja2Templates(
        directory=f"{app_config().WEBCONTENT_PATH}/admin/templates"
    )

    # @security: role=admin
    @admin_router.get("/", response_class=HTMLResponse,
                      include_in_schema=False)
    def home(request: Request,
             sec_ctx: Annotated[SecurityContext, Depends(web_basic_context)]
             ):
        logger.debug("home")
        security_check(rolename=Rolename.ADMIN)
        return _templates.TemplateResponse("home.j2", {"request": request})

    # @security: role=admin
    @admin_router.get("/create_token", response_class=HTMLResponse,
                      include_in_schema=False)
    def create_token(
            request: Request,
            sec_ctx: Annotated[SecurityContext, Depends(web_basic_context)]
    ):
        logger.debug("create_token")
        security_check(rolename=Rolename.ADMIN)
        return _templates.TemplateResponse("create_token.j2", {
            "request": request,
            "expire_sec": app_settings().TOKEN_EXPIRE_SEC,
        })

    # @security: role=admin
    @admin_router.post('/create_token_ctl', response_class=PlainTextResponse,
                       include_in_schema=False)
    def create_token_ctl(
            request: Request,
            sec_ctx: Annotated[SecurityContext, Depends(web_basic_context)],
            username: Annotated[str, Form()],
            expire_sec: Annotated[int, Form()]):
        logger.debug("create_token_ctl")
        security_check(rolename=Rolename.ADMIN)
        res: Token = SecSysService().create_access_token(username, expire_sec)
        return PlainTextResponse(content=res.access_token)

    # @security: role=admin
    @admin_router.get("/password_hash", response_class=HTMLResponse,
                      include_in_schema=False)
    def password_hash(
            request: Request,
            sec_ctx: Annotated[SecurityContext, Depends(web_basic_context)],
    ):
        logger.debug("password_hash")
        security_check(rolename=Rolename.ADMIN)
        return _templates.TemplateResponse("password_hash.j2", {
            "request": request,
        })

    # @security: role=admin
    @admin_router.post('/password_hash_ctl', response_class=PlainTextResponse,
                       include_in_schema=False)
    def password_hash_ctl(
            request: Request,
            sec_ctx: Annotated[SecurityContext, Depends(web_basic_context)],
            password: Annotated[str, Form()]):
        logger.debug("password_hash_ctl")
        security_check(rolename=Rolename.ADMIN)
        res: str = SecSysService().get_password_hash(password)
        return PlainTextResponse(content=res)

    # @security: role=admin
    @admin_router.get("/send_fmessage", response_class=HTMLResponse,
                      include_in_schema=False)
    def send_fmessage(
            request: Request,
            sec_ctx: Annotated[SecurityContext, Depends(web_basic_context)]
    ):
        logger.debug("send_fmessage")
        security_check(rolename=Rolename.ADMIN)
        dao: DAO = DAO()
        levels = dao.message.get_message_levels()
        logger.debug(f"levels={str(levels)}")
        providers = dao.message.get_data_providers()
        logger.debug(f"providers={str(providers)}")
        return _templates.TemplateResponse("send_fmessage.j2", {
            "request": request,
            "username": security_context().username,
            "levels": levels,
            "providers": providers
        })

    # @security: role=admin
    @admin_router.post('/send_fmessage_ctl', response_class=PlainTextResponse,
                       include_in_schema=False)
    def send_fmessage_ctl(
            request: Request,
            sec_ctx: Annotated[SecurityContext, Depends(web_basic_context)],
            username: Annotated[str, Form()],
            study_id: Annotated[int, Form()],
            level_id: Annotated[int, Form()],
            provider_id: Annotated[int, Form()],
            description: Annotated[str, Form()],
            payload: Annotated[str, Form()]
    ):
        logger.debug("send_fmessage_ctl")
        security_check(rolename=Rolename.ADMIN)
        msg: MessageLogEntity = MessageService().send_message(
            username,
            study_id,
            None,
            MessageCategoryId.FEEDBACK,
            level_id,
            1,
            provider_id,
            description,
            payload
        )
        return PlainTextResponse(
            content=f"Done: {json.dumps(msg.to_dict(), indent=4)}")

    # @security: role=admin
    @admin_router.get("/username_by_token", response_class=HTMLResponse,
                      include_in_schema=False)
    def username_by_token(
            request: Request,
            sec_ctx: Annotated[SecurityContext, Depends(web_basic_context)]
    ):
        logger.debug("username_by_token")
        security_check(rolename=Rolename.ADMIN)
        return _templates.TemplateResponse("username_by_token.j2", {
            "request": request,
        })

    # @security: role=admin
    @admin_router.post('/username_by_token_ctl', response_class=PlainTextResponse,
                       include_in_schema=False)
    def username_by_token_ctl(
            request: Request,
            sec_ctx: Annotated[SecurityContext, Depends(web_basic_context)],
            token: Annotated[str, Form()]
    ):
        logger.debug("username_by_token_ctl")
        security_check(rolename=Rolename.ADMIN)
        res: str = SecSysService().get_username_by_token(token)
        return PlainTextResponse(content=res)

    # @security: role=admin
    @admin_router.get('/view_config', response_class=PlainTextResponse,
                      include_in_schema=False)
    def view_config(
            request: Request,
            sec_ctx: Annotated[SecurityContext, Depends(web_basic_context)]
    ):
        logger.debug("view_config")
        security_check(rolename=Rolename.ADMIN)
        return PlainTextResponse(
            content=json.dumps(app_config().to_dict(), indent=4))

    return admin_router
