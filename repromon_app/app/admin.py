import json
import logging
from flask import render_template, make_response, jsonify, Blueprint, request
from repromon_app.config import app_config
from repromon_app.dao import DAO
from repromon_app.model import MessageLevelEntity, MessageLogEntity, MessagePayloadEntity, DataProviderEntity, \
    MessageCategory

from repromon_app.security import security_context
from repromon_app.service import MessageService

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
@admin_bp.route('/send_fmessage')
def send_fmessage():
    logger.debug("send_fmessage")
    dao: DAO = DAO()
    levels = dao.message.get_message_levels()
    logger.debug("levels="+str(levels))
    providers = dao.message.get_data_providers()
    logger.debug("providers="+str(providers))
    return render_template(
        'admin/send_fmessage.j2',
        username=security_context().username,
        levels=levels,
        providers=providers
    )


# @security: role=admin
@admin_bp.route('/send_fmessage_ctl', methods=['GET', 'POST'])
def send_fmessage_ctl():
    logger.debug("send_fmessage_ctl")
    un = request.form["username"]
    logger.debug("un="+un)
    msg: MessageLogEntity = MessageService().send_message(
        str(request.form["username"]),
        int(request.form["study_id"]),
        MessageCategory.ID_FEEDBACK,
        int(request.form["level_id"]),
        int(request.form["provider_id"]),
        str(request.form["description"]),
        str(request.form["payload"])
    )
    return response_ok('Done: '+json.dumps(msg.to_dict(), indent=4), 'text/plain')


# @security: role=admin
@admin_bp.route('/view_config')
def view_config():
    logger.debug("view_config")
    return response_ok(json.dumps(app_config().to_dict(), indent=4), 'text/plain')
