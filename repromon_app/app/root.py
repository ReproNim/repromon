import json
import logging
from datetime import datetime
from flask import render_template, make_response, jsonify, Blueprint, request
from repromon_app.config import app_config
from repromon_app.dao import DAO
from repromon_app.service import LoginService, FeedbackService

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


# @security: role=data_collector, auth
@root_bp.route('/feedback_screen', methods=['GET'])
def feedback_screen():
    logger.debug("feedback_screen")

    #study_id = int(request.form["study_id"])
    study_id = int(request.args.get("study_id"))
    logger.debug(f"study_id={study_id}")
    feedback_service = FeedbackService()
    ts = datetime.now()
    current_user = LoginService().get_current_user()
    return render_template('root/feedback_screen.j2',
                           study_id=study_id,
                           feedback_service=feedback_service,
                           current_user=current_user,
                           ts=ts
                           )
