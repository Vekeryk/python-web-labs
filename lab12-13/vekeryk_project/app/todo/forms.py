from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from wtforms import StringField, SubmitField, TextAreaField, SelectField, SelectMultipleField, DateField
from wtforms.validators import DataRequired, Length
from .models import Category, Priority, Progress
from ..account.models import User


class TaskCreateForm(FlaskForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.category.choices = [(elem.id, elem.name)
                                 for elem in Category.query.all()]
        self.collaborators.choices = [
            (elem.id, elem.username) for elem in User.query.all()]

    title = StringField(
        'Title',
        validators=[DataRequired(message='Field cannot be empty!')]
    )
    description = CKEditorField(
        'Description',
        validators=[
            DataRequired(),
            Length(min=3, message='Field must be min 3 characters long!')
        ],
        render_kw={"class": ""}
    )
    priority = SelectField(
        'Priority',
        choices=[(name, name) for name in Priority._member_names_],
        render_kw={"class": "form-select"}
    )
    category = SelectField(
        'Category',
        coerce=int,
        render_kw={"class": "form-select"}
    )
    collaborators = SelectMultipleField(
        'User',
        coerce=int,
        render_kw={"class": "form-select"}
    )
    deadline = DateField(
        'Deadline', 
        validators=[DataRequired()], 
        render_kw={"class": "my-2"}
    )

    submit = SubmitField('Submit')


class TaskUpdateForm(TaskCreateForm, FlaskForm):
    progress = SelectField(
        'Progress',
        choices=[(name, name) for name in Progress._member_names_],
        render_kw={"class": "form-select"}
    )


class CategoryForm(FlaskForm):
    name = StringField(
        'Name',
        validators=[DataRequired(message='Field cannot be empty!')]
    )
    submit = SubmitField('Submit')


class CommentForm(FlaskForm):
    body = CKEditorField(
        'Comment', 
        [DataRequired(message='Field cannot be empty!')])
    
    submit = SubmitField('Send')