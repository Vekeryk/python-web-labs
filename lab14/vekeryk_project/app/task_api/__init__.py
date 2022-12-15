from flask import Blueprint
from flask_restful import Api

task_api_bp = Blueprint('task_api', __name__)
api = Api(task_api_bp)

from . import views
