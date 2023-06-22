import logging
import logging.config
from pathlib import Path
from flask import Flask, render_template

logger = logging.getLogger(__name__)
# init logger, will be moved outside
logFile = str(Path(__file__).parent.parent) + '/logging.ini'
logging.config.fileConfig(logFile, disable_existing_loggers=False)
logger.debug("name=" + __name__)


def create_flask_app() -> Flask:
    """ Creates basic flask webapp

    :return: Root flask webapp
    """
    logger.info("create_flask_app()")

    app_web = Flask(__name__, template_folder='app/web/templates', static_folder='app/web/static')

    @app_web.route('/')
    def home():
        logger.debug("home")
        return render_template('home.j2')

    return app_web


def main():
    app = create_flask_app()
    logger.debug("Running server ...")
    app.run(use_reloader=False, port=9095)


if __name__ == "__main__":
    main()
