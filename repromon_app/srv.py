import logging
import logging.config
from pathlib import Path
from flask import Flask, render_template
from repromon_app.cfg import app_config, app_config_init
from repromon_app.db import db_init, db_session_done
from repromon_app.app.admin import admin_bp
from repromon_app.app.test import test_bp

logger = logging.getLogger(__name__)
logger.debug("name=" + __name__)


def create_flask_app() -> Flask:
    """ Creates basic flask webapp

    :return: Root flask webapp
    """
    app_config_init()
    logger.info("create_flask_app()")

    logger.debug("Initialize DB...")
    # ?? db_init(app_config().db.dict(), threading.get_ident)
    db_init(app_config().db.dict())

    app_web: Flask = Flask(__name__, template_folder='app/web/templates', static_folder='app/web/static')
    app_web.config.from_mapping(app_config().flask.dict())

    # register blueprints
    with app_web.app_context():
        logger.debug("Registering blueprint: admin ...")
        app_web.register_blueprint(admin_bp, url_prefix='/admin')

        logger.debug("Registering blueprint: test ...")
        app_web.register_blueprint(test_bp, url_prefix='/test')


    @app_web.teardown_appcontext
    def teardown_appcontext(resp_or_exc):
        # logger.debug("teardown_appcontext(...)")
        db_session_done()

    # @security: any
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
