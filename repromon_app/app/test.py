import logging

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from repromon_app.config import app_config
from repromon_app.dao import DAO

logger = logging.getLogger(__name__)
logger.debug(f"name={__name__}")


def create_test_router() -> APIRouter:
    test_router = APIRouter()
    _templates = Jinja2Templates(
        directory=f"{app_config().WEB_PATH}/templates/test")

    # @security: env=dev|qa|uat, auth, ??role=tester
    @test_router.get("/", response_class=HTMLResponse)
    def home(request: Request):
        logger.debug("home")
        return _templates.TemplateResponse("home.j2", {"request": request})

    # @security: env=dev|qa|uat, auth, ??role=tester
    @test_router.get('/test1', response_class=HTMLResponse)
    def test1(request: Request):
        logger.debug("test1")
        dao: DAO = DAO()

        roles = dao.account.get_roles()
        logger.debug(f"roles={str(roles)}")

        role_infos = dao.account.get_role_infos()
        logger.debug(f"role_infos={str(role_infos)}")

        return HTMLResponse("Done")

    return test_router
