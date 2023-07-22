import json
import logging
from typing import Annotated

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from repromon_app.config import app_config
from repromon_app.dao import DAO
from repromon_app.model import MessageCategory, MessageLogEntity, Rolename
from repromon_app.security import security_check, security_context
from repromon_app.service import MessageService

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
    def home(request: Request):
        logger.debug("home")
        security_check(rolename=Rolename.ADMIN)
        return _templates.TemplateResponse("home.j2", {"request": request})

    # @security: role=admin
    @admin_router.get("/send_fmessage", response_class=HTMLResponse,
                      include_in_schema=False)
    def send_fmessage(request: Request):
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
    def send_fmessage_ctl(username: Annotated[str, Form()],
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
            MessageCategory.ID_FEEDBACK,
            level_id,
            provider_id,
            description,
            payload
        )
        return PlainTextResponse(
            content=f"Done: {json.dumps(msg.to_dict(), indent=4)}")

    # @security: role=admin
    @admin_router.get('/view_config', response_class=PlainTextResponse,
                      include_in_schema=False)
    def view_config():
        logger.debug("view_config")
        security_check(rolename=Rolename.ADMIN)
        return PlainTextResponse(
            content=json.dumps(app_config().to_dict(), indent=4))

    return admin_router
