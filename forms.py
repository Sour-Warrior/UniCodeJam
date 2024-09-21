from wtforms import StringField, SelectField, SubmitField
from wtforms.form import Form
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired

# For some dang reason, instances of SearchForm or any subclass of Form or FlaskForm won't show any attributes or methods of both itself and those of both parent classes
# In the unlikely scenario that someone is reading this, do you know any fixes for this? Quite a hair-pulling issue
class SearchForm(Form):
    search = StringField("search", validators=[DataRequired()])
    submit = SubmitField("submit")
