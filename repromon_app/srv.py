import logging
import logging.config
from pathlib import Path
from flask import Flask, render_template
from repromon_app.cfg import app_cfg, app_cfg_init

logger = logging.getLogger(__name__)
logger.debug("name=" + __name__)


def create_flask_app() -> Flask:
    """ Creates basic flask webapp

    :return: Root flask webapp
    """
    app_cfg_init()
    logger.info("create_flask_app()")

    app_web: Flask = Flask(__name__, template_folder='app/web/templates', static_folder='app/web/static')
    app_web.config.from_mapping(app_cfg().FLASK.dict())

    @app_web.route('/')
    def home():
        logger.debug("home")
        return render_template('home.j2')

    return app_web


def main():
    app = create_flask_app()
    logger.debug("Running server ...")
    app.run(use_reloader=False)


if __name__ == "__main__":
    main()
