import json
import logging
from flask import render_template, make_response, jsonify, Blueprint
from repromon_app.cfg import app_config

logger = logging.getLogger(__name__)
logger.debug("name=" + __name__)

test_bp = Blueprint('test_bp', __name__)


def response_ok(res, mimetype):
    response = make_response(res, 200)
    response.mimetype = mimetype
    return response


@test_bp.route('/')
def home():
    logger.debug("home")
    return render_template('test/home.j2')


@test_bp.route('/test1')
def view_config():
    logger.debug("test1")
    return response_ok("Done", 'text/plain')
