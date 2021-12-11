from flask_wtf import FlaskForm
from wtforms import SearchField,SelectField,SubmitField,StringField,FileField,BooleanField,\
    DateField,DateTimeField,SelectMultipleField,PasswordField,MultipleFileField
from wtforms.validators import DataRequired, Email, Length

class SomeForm(FlaskForm):
    search=SearchField('Search')
    select=SelectField('Select')
    submit=SubmitField('Submit')
    email=StringField('Email',validators=[Email()])
    file=FileField('file')
    boolean=BooleanField('remember')
    date=DateField('Date')
    datetime=DateTimeField('DateTime')
    multiplefield=SelectMultipleField('SelectMultipleField')
    password=PasswordField('Password', validators=[DataRequired(), Length(min=4,max=100)])
    multfile=MultipleFileField('MultipleFileField')

    strategy = BooleanField('Strategy')
    adventure = BooleanField('Adventure')
    action = BooleanField('Action')
    survival = BooleanField('Survival')
    rpg = BooleanField('RPG')
    fps = BooleanField('FPS')
