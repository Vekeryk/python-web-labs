from flask_restful import Resource, reqparse, fields, marshal_with
from flask import abort
from ..todo.models import Priority, Progress, Task
from . import api
from ..import db

task_create = reqparse.RequestParser()
task_create.add_argument('title', type=str, help='Title is required', required=True)
task_create.add_argument('description', type=str, help='Description is required', required=True)
task_create.add_argument('priority', type=str, help='Priority is required', required=True)
task_create.add_argument('category_id', type=int, help='Category id is required', required=True)
task_create.add_argument('owner_id', type=int, help='Owner id is required', required=True)

task_update = reqparse.RequestParser()
task_update.add_argument('title', type=str)
task_update.add_argument('description', type=str)
task_update.add_argument('priority', type=str)
task_update.add_argument('progress', type=str)
task_update.add_argument('category_id', type=int)
task_update.add_argument('owner_id', type=int)

resource_fields = {
    'id' : fields.Integer,
    'title' : fields.String,
    'description': fields.String,
    'priority' : fields.String(attribute=lambda x: str(Priority(x.priority).name)),
    'progress' : fields.String(attribute=lambda x: str(Progress(x.progress).name)),
    'created' : fields.String,
    'deadline' : fields.String,
}

class TaskApi(Resource):
    @marshal_with(resource_fields)
    def get(self, todo_id=None):
        if todo_id is None:
            tasks = Task.query.all()
            return tasks

        task = Task.query.get_or_404(todo_id)
        return task, 200


    @marshal_with(resource_fields)
    def post(self):
        data = task_create.parse_args()

        new_task = Task(title=data.get('title'), 
                        description=data.get('description'),
                        priority=data.get('priority'),
                        category_id=data.get('category_id'),
                        owner_id=data.get('owner_id')) 

        try:
            db.session.add(new_task)
            db.session.commit()
        except:
            db.session.rollback()
            abort(500, 'Server error')

        task = Task.query.all()[-1]
        return task, 201


    @marshal_with(resource_fields)
    def put(self, todo_id):
        data = task_update.parse_args()

        task = Task.query.get_or_404(todo_id)
        if data.get('title'):
            task.title = data.get('title')
        if data.get('description'):
            task.description = data.get('description')
        if data.get('priority'):
            task.priority = data.get('priority')
        if data.get('progress'):
            task.progress = data.get('progress')
        if data.get('category_id'):
            task.category_id = data.get('category_id')
        if data.get('owner_id'):
            task.owner_id = data.get('owner_id')

        try:
            db.session.commit()
        except:
            db.session.rollback()
            abort(500, 'Server error')

        task = Task.query.get_or_404(todo_id)
        return task, 200


    def delete(self, todo_id):
        task = Task.query.get_or_404(todo_id)
        try:
            db.session.delete(task)
            db.session.commit()
        except:
            db.session.rollback()
            abort(500, 'Server error')

        return '', 204


api.add_resource(TaskApi, '/<string:todo_id>', '/')