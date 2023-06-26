import json
import logging
from flask import render_template, make_response, jsonify, Blueprint
from repromon_app.config import app_config

logger = logging.getLogger(__name__)
logger.debug("name=" + __name__)

admin_bp = Blueprint('admin_bp', __name__)


def response_ok(res, mimetype):
    response = make_response(res, 200)
    response.mimetype = mimetype
    return response


# @security: role=admin
@admin_bp.route('/')
def home():
    logger.debug("home")
    return render_template('admin/home.j2')


# @security: role=admin
@admin_bp.route('/view_config')
def view_config():
    logger.debug("view_config")
    return response_ok(json.dumps(app_config().to_dict(), indent=4), 'text/plain')
