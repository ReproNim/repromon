import logging
from datetime import datetime

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from repromon_app.config import app_config
from repromon_app.service import FeedbackService, LoginService

logger = logging.getLogger(__name__)
logger.debug(f"name={__name__}")


def create_app_router() -> APIRouter:
    app_router = APIRouter()
    app_router.mount("/static", StaticFiles(
        directory=f"{app_config().WEBCONTENT_PATH}/static"), name="static")
    _templates = Jinja2Templates(
        directory=f"{app_config().WEBCONTENT_PATH}/app/templates")

    # @security: any
    @app_router.get("/", response_class=HTMLResponse, include_in_schema=False)
    def home(request: Request):
        logger.debug("home")
        return _templates.TemplateResponse("home.j2", {"request": request})

    # @security: any
    @app_router.get("/current_user", response_class=JSONResponse,
                    include_in_schema=False)
    def current_user(request: Request):
        logger.debug("current_user")
        return JSONResponse(content=LoginService().get_current_user().dict())

    # @security: role=data_collector, auth
    @app_router.get("/feedback_screen", response_class=HTMLResponse,
                    include_in_schema=False
                    )
    def feedback_screen(request: Request, study_id: int):
        logger.debug("feedback_screen")

        # study_id = int(request.form["study_id"])
        # study_id = int(request.args.get("study_id"))
        logger.debug(f"study_id={study_id}")
        feedback_service = FeedbackService()
        ts = datetime.now()
        cu = LoginService().get_current_user()
        return _templates.TemplateResponse("feedback_screen.j2", {
            "request": request,
            "study_id": study_id,
            "feedback_service": feedback_service,
            "current_user": cu,
            "ts": ts
        })

    return app_router
