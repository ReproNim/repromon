import logging
import logging.config

import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from repromon_app.app.admin import create_admin_router
from repromon_app.app.root import create_root_router
from repromon_app.app.test import create_test_router
from repromon_app.config import app_config, app_config_init
from repromon_app.db import db_init

logger = logging.getLogger(__name__)
logger.debug(f"name={__name__}")


def create_fastapi_app() -> FastAPI:
    app_config_init()
    logger.info("create_fastapi_app()")

    logger.debug("Initialize DB...")
    # ?? db_init(app_config().db.dict(), threading.get_ident)
    db_init(app_config().db.dict())

    app_web = FastAPI()
    # app_web.add_middleware(SessionMiddleware, secret_key="RNRPID")

    # Configure static files (CSS, JavaScript, etc.)
    app_web.mount("/static", StaticFiles(
        directory=f"{app_config().WEB_PATH}/static"), name="static")

    logger.debug("Registering router: /root ...")
    app_web.include_router(create_root_router(), prefix="/root")

    logger.debug("Registering router: /admin ...")
    app_web.include_router(create_admin_router(), prefix="/admin")

    logger.debug("Registering router: /test ...")
    app_web.include_router(create_test_router(), prefix="/test")

    # TODO: auto commit/rollback DB session using db_session_done
    # under async fastapi execution context

    @app_web.get("/", include_in_schema=False)
    async def root():
        # url = app.url_path_for("root")
        return RedirectResponse(url='/root')

    return app_web


def main():
    logger.info("Running server ...")
    app = create_fastapi_app()
    uvicorn.run(app, **app_config().uvicorn.dict())
    logger.info("Server stopped.")


if __name__ == "__main__":
    main()
