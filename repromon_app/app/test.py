import logging

from flask import Blueprint, make_response, render_template

from repromon_app.dao import DAO

logger = logging.getLogger(__name__)
logger.debug(f"name={__name__}")

test_bp = Blueprint('test_bp', __name__)


def response_ok(res, mimetype):
    response = make_response(res, 200)
    response.mimetype = mimetype
    return response


# @security: env=dev|qa|uat, auth, ??role=tester
@test_bp.route('/')
def home():
    logger.debug("home")
    return render_template('test/home.j2')


# @security: env=dev|qa|uat, auth, ??role=tester
@test_bp.route('/test1')
def test1():
    logger.debug("test1")
    dao: DAO = DAO()

    roles = dao.account.get_roles()
    logger.debug(f"roles={str(roles)}")

    role_infos = dao.account.get_role_infos()
    logger.debug(f"role_infos={str(role_infos)}")

    return response_ok("Done", 'text/plain')
