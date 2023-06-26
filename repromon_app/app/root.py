import json
import logging
from flask import render_template, make_response, jsonify, Blueprint
from repromon_app.cfg import app_config
from repromon_app.dao import DAO
from repromon_app.svc import LoginService

logger = logging.getLogger(__name__)
logger.debug("name=" + __name__)

root_bp = Blueprint('root_bp', __name__)


def response_ok(res, mimetype):
    response = make_response(res, 200)
    response.mimetype = mimetype
    return response


# @security: any
@root_bp.route('/')
def home():
    logger.debug("home")
    return render_template('root/home.j2')


# @security: any
@root_bp.route('/current_user')
def current_user():
    logger.debug("current_user")
    return response_ok(LoginService().get_current_user().json(), 'application/json')
