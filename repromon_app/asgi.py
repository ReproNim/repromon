import logging

from fastapi import FastAPI

from repromon_app.srv import create_fastapi_app

logger = logging.getLogger(__name__)

# Entry point for ASGI, e.g. for uvicorn can be started locally as:
# > uvicorn repromon_app.asgi:app --host 127.0.0.1 --port 5050
app: FastAPI = create_fastapi_app()
