import logging.config
import os
from typing import Annotated

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from starlette.datastructures import Headers

from repromon_app.config import app_config, app_config_init, app_settings
from repromon_app.db import db_init
from repromon_app.router.admin import create_admin_router
from repromon_app.router.api_v1 import create_api_v1_router
from repromon_app.router.app import create_app_router
from repromon_app.router.test import create_test_router
from repromon_app.security import SecurityManager, Token, current_web_request

logger = logging.getLogger(__name__)
logger.debug(f"name={__name__}")


class NoCacheStaticFiles(StaticFiles):
    def is_not_modified(
        self, response_headers: Headers, request_headers: Headers
    ) -> bool:
        return False


def create_fastapi_app() -> FastAPI:
    app_config_init()
    logger.info("create_fastapi_app()")

    logger.debug("Initialize DB...")
    # ?? db_init(app_config().db.dict(), threading.get_ident)
    db_init(app_config().db.dict())

    app_web = FastAPI(
        title="ReproMon App",
        description="ReproMon Web Application REST API v1",
        version="1.0.0",
        openapi_tags=[
            {
                "name": "AccountService",
                "description": "AccountService admin operations."
            },
            {
                "name": "FeedbackService",
                "description": "FeedbackService operations."
            },
            {
                "name": "LoginService",
                "description": "LoginService operations."
            },
            {
                "name": "MessageService",
                "description": "MessageService operations."
            },
            {
                "name": "SecSysService",
                "description": "SecSysService operations."
            },
        ]
    )
    # app_web.add_middleware(SessionMiddleware, secret_key="RNRPID")
    # configure CORS to allow REST calls from rich frontend
    app_web.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",
            "https://localhost:3000",
            "http://localhost:4200",
            "https://localhost:4200",
            "http://localhost:9095",
            "https://localhost:9095",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Configure static files (CSS, JavaScript, etc.)
    app_web.mount("/static", StaticFiles(
        directory=f"{app_config().WEBCONTENT_PATH}/static"), name="static")

    # Configure RIA /ui web content
    ui_path: str = app_settings().UI_APP_PATH
    if ui_path and os.path.exists(ui_path):
        logger.debug(f"Registering RIA app: /ui ... {str(ui_path)}")
        app_web.mount("/ui", NoCacheStaticFiles(
            directory=ui_path,
            html=True
        ), name="ui")
    else:
        logger.error(f"RIA /ui web content not found: {str(ui_path)}")

    # Configure RIA /ui2 web content
    ui2_path: str = app_settings().UI2_APP_PATH
    if ui2_path and os.path.exists(ui2_path):
        logger.debug(f"Registering RIA app: /ui2 ... {str(ui2_path)}")
        app_web.mount("/ui2", NoCacheStaticFiles(
            directory=ui2_path,
            html=True
        ), name="ui2")
    else:
        logger.error(f"RIA /ui2 web content not found: {str(ui2_path)}")

    logger.debug("Registering router: /api/1 ...")
    app_web.include_router(create_api_v1_router(), prefix="/api/1")

    logger.debug("Registering router: /app ...")
    app_web.include_router(create_app_router(), prefix="/app")

    logger.debug("Registering router: /admin ...")
    app_web.include_router(create_admin_router(), prefix="/admin")

    logger.debug("Registering router: /test ...")
    app_web.include_router(create_test_router(), prefix="/test")

    @app_web.get("/", include_in_schema=False)
    async def app_root():
        # url = app.url_path_for("app")
        return RedirectResponse(url='/app')

    @app_web.post("/token", include_in_schema=False,
                  response_model=Token)
    async def app_token(
            form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
    ):
        mgr: SecurityManager = SecurityManager.instance()
        try:
            if not mgr.auth_user(form_data.username, form_data.password):
                raise Exception("Auth failed")
        except BaseException as ex1:
            logger.debug(f"Auth failed: {str(ex1)}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(ex1),
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token: str = mgr.create_access_token(form_data.username)
        res: Token = Token(access_token=access_token, token_type="bearer")
        return res

    @app_web.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, e: Exception):
        # protect some bugs in fastapi/pydantic with ValidationError
        detail: str = None
        try:
            detail = str(e)
        except BaseException:
            detail = "Internal unhandled server error"

        logger.error(f"Unhandled exception: {detail}")
        return JSONResponse(
            status_code=500,
            content={"detail": detail}
        )

    @app_web.middleware("http")
    async def app_request_context(request: Request, call_next):
        # TODO: auto commit/rollback DB session using db_session_done
        # under async fastapi execution context

        # logger.debug(f"app_request_context enter: {request.url}")
        # request.state.custom_data = {"key": "value"}
        current_web_request.set(request)
        response = await call_next(request)
        # logger.debug(f"app_request_context leave: {request.url}")
        return response

    return app_web


def main():
    logger.info("Running server ...")
    app = create_fastapi_app()
    uvicorn.run(app, **app_config().uvicorn.dict())
    logger.info("Server stopped.")


if __name__ == "__main__":
    main()
