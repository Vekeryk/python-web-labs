from flask import render_template, request, redirect, flash, url_for
from flask_login import current_user, login_required

from .. import db
from ..account.models import User
from .models import Comment, Task, Category
from .forms import CategoryForm, CommentForm, TaskCreateForm, TaskUpdateForm
from . import todo_bp


@todo_bp.route("/task-list/<user_id>")
def tasks(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('tasks.html', user=user)


@todo_bp.route("/tasks/<task_id>", methods=['GET', 'POST'])
@login_required
def task(task_id):
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(
            body=form.body.data, 
            user_id=current_user.id,
            task_id=task_id
        )
        try:
            db.session.add(comment)
            db.session.commit()
            flash(f"Added new comment", category='success')
        except:
            db.session.flush()
            db.session.rollback()

    task = Task.query.get_or_404(task_id)
    return render_template('task.html', task=task, form=form)


@todo_bp.route("/categories")
def categories():
    categories = Category.query.all()
    return render_template('categories.html', categories=categories)


@todo_bp.route("/categories/create", methods=['GET', 'POST'])
@login_required
def create_category():
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(name=form.name.data)
        try:
            db.session.add(category)
            db.session.commit()
        except:
            db.session.flush()
            db.session.rollback()
        flash(f"New category created: {form.name.data}", category='success')
        return redirect(url_for("todo.categories"))
    elif request.method == 'POST':
        flash("Validation failed", category='warning')

    return render_template('create_category.html', form=form)


@todo_bp.route("/tasks/create", methods=['GET', 'POST'])
@login_required
def create_task():
    form = TaskCreateForm()
    if form.validate_on_submit():
        task = Task(
            title=form.title.data,
            description=form.description.data,
            priority=form.priority.data,
            category_id=form.category.data,
            owner_id=current_user.id,
            deadline=form.deadline.data
        )
        try:
            for collaborator in form.collaborators.data:
                task.collaborators.append(User.query.get_or_404(collaborator))
            db.session.add(task)
            db.session.commit()
            flash(f"New task created: {form.title.data}", category='success')
            return redirect(url_for("todo.tasks", user_id=current_user.id))
        except:
            db.session.flush()
            db.session.rollback()
            flash(f"Unknown error", category='danger')
    elif request.method == 'POST':
        flash("Validation failed", category='warning')

    return render_template('create_task.html', form=form)


@todo_bp.route('/categories/<id>/delete')
@login_required
def delete_category(id):
    category = Category.query.get_or_404(id)
    try:
        db.session.delete(category)
        db.session.commit()
        flash(f"Category has been deleted", category='success')
    except:
        db.session.flush()
        db.session.rollback()
    return redirect(url_for("todo.categories"))


@todo_bp.route('/tasks/<id>/delete')
@login_required
def delete_task(id):
    print(id)
    task = Task.query.get_or_404(id)
    try:
        db.session.delete(task)
        db.session.commit()
        flash(f"Task has been deleted", category='success')
    except:
        db.session.flush()
        db.session.rollback()
    return redirect(url_for("todo.tasks", user_id=current_user.id))


@todo_bp.route("/tasks/<id>/update", methods=['GET', 'POST'])
@login_required
def update_task(id):
    task = Task.query.get_or_404(id)
    form = TaskUpdateForm()

    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.priority = form.priority.data
        task.progress = form.progress.data
        task.category_id = form.category.data
        task.deadline = form.deadline.data

        try:
            task.collaborators.clear()
            for collaborator in form.collaborators.data:
                task.collaborators.append(User.query.get_or_404(collaborator))
            db.session.commit()
            flash(
                f"Task has been updated: {form.title.data}", category='success')
            return redirect(url_for("todo.tasks", user_id=current_user.id))
        except:
            db.session.flush()
            db.session.rollback()
            flash(f"Unknown error", category='danger')
            return render_template('update_task.html', form=form, id=id)
    elif request.method == 'POST':
        flash("Validation failed", category='warning')

    form.title.data = task.title
    form.description.data = task.description
    form.priority.data = task.priority.name
    form.progress.data = task.progress.name
    form.category.data = task.category_id
    form.collaborators.data = [
        collaborator.id for collaborator in task.collaborators]
    form.deadline.data = task.deadline
    return render_template('update_task.html', form=form, id=id)


@todo_bp.route("/categories/<id>/update", methods=['GET', 'POST'])
@login_required
def update_category(id):
    category = Category.query.get_or_404(id)
    form = CategoryForm()

    if form.validate_on_submit():
        category.name = form.name.data
        try:
            db.session.add(category)
            db.session.commit()
            flash(
                f"Category has been updated: {form.name.data}", category='success')
            return redirect(url_for("todo.categories"))
        except:
            db.session.flush()
            db.session.rollback()
            flash(f"Unknown error", category='danger')
            return render_template('update_category.html', form=form, id=id)
    elif request.method == 'POST':
        flash("Validation failed", category='warning')

    form.name.data = category.name
    return render_template('update_category.html', form=form, id=id)
