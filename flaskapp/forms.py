from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class MovieForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    genres = StringField('Genres', validators=[DataRequired()])
    rating = StringField('Rating', validators=[DataRequired()])
    duration = StringField('Duration', validators=[DataRequired()])
    quality = StringField('Quality', validators=[DataRequired()])
    trailer = StringField('Trailer', validators=[DataRequired()])
    watch = StringField('Watch', validators=[DataRequired()])
    submit = SubmitField('Add')


class SearchForm(FlaskForm):
    searched = StringField('Searched', validators=[DataRequired()])
    submit = SubmitField('Submit')
