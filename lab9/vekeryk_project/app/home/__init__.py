from flask import Blueprint

home_bp = Blueprint('home', __name__,
                        template_folder='templates/home')

from . import views