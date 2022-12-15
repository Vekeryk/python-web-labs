from flask import Blueprint

category_api_bp = Blueprint('category_api', __name__)

from . import views
