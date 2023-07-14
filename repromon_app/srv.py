import logging.config
import os

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from repromon_app.config import app_config, app_config_init, app_settings
from repromon_app.db import db_init
from repromon_app.router.admin import create_admin_router
from repromon_app.router.api_v1 import create_api_v1_router
from repromon_app.router.app import create_app_router
from repromon_app.router.test import create_test_router

logger = logging.getLogger(__name__)
logger.debug(f"name={__name__}")


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
                "name": "LoginService",
                "description": "LoginService operations."
            },
            {
                "name": "FeedbackService",
                "description": "FeedbackService operations."
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
        app_web.mount("/ui", StaticFiles(
            directory=ui_path), name="ui")
    else:
        logger.error(f"RIA /ui web content not found: {str(ui_path)}")

    logger.debug("Registering router: /api/1 ...")
    app_web.include_router(create_api_v1_router(), prefix="/api/1")

    logger.debug("Registering router: /app ...")
    app_web.include_router(create_app_router(), prefix="/app")

    logger.debug("Registering router: /admin ...")
    app_web.include_router(create_admin_router(), prefix="/admin")

    logger.debug("Registering router: /test ...")
    app_web.include_router(create_test_router(), prefix="/test")

    # TODO: auto commit/rollback DB session using db_session_done
    # under async fastapi execution context

    @app_web.get("/", include_in_schema=False)
    async def app_root():
        # url = app.url_path_for("app")
        return RedirectResponse(url='/app')

    return app_web


def main():
    logger.info("Running server ...")
    app = create_fastapi_app()
    uvicorn.run(app, **app_config().uvicorn.dict())
    logger.info("Server stopped.")


if __name__ == "__main__":
    main()
