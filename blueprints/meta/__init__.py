from quart import Blueprint

meta_bp = Blueprint("meta", __name__)

from . import routes
