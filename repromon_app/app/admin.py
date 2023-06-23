import logging
from flask import render_template, Blueprint

logger = logging.getLogger(__name__)
logger.debug("name=" + __name__)

admin_bp = Blueprint('admin_bp', __name__)


@admin_bp.route('/')
def home():
    logger.debug("home")
    return render_template('admin/home.j2')

