from flask_wtf import FlaskForm
from wtforms import  SelectField, SubmitField, StringField, FileField, BooleanField, \
    DateField, DateTimeField, SelectMultipleField, PasswordField, MultipleFileField, TextAreaField
from wtforms.validators import DataRequired, Email, Length


class SomeForm(FlaskForm):
    # search=SearchField('Search')
    # select=SelectField('Select')
    # submit=SubmitField('Submit')
    # email=StringField('Email',validators=[Email()])
    # file=FileField('file')
    # boolean=BooleanField('remember')
    # date=DateField('Date')
    # datetime=DateTimeField('DateTime')
    # multiplefield=SelectMultipleField('SelectMultipleField')
    # password=PasswordField('Password', validators=[DataRequired(), Length(min=4,max=100)])
    # multfile=MultipleFileField('MultipleFileField')

    strategy = BooleanField('Strategy')
    adventure = BooleanField('Adventure')
    action = BooleanField('Action')
    survival = BooleanField('Survival')
    rpg = BooleanField('RPG')
    fps = BooleanField('FPS')
    search = StringField('Search', id='search', validators=[DataRequired(), Length(min=3)])
    login_user_name = StringField('User name', id='login_user_name',
                                  validators=[DataRequired(), Length(min=3)])
    login_password = PasswordField('Password', id='login_password',
                                   validators=[DataRequired(), Length(min=4, max=100)])
    login_submit = SubmitField('Sign in', id='sign-in')
    remember_me = BooleanField('Remember me')
    username = StringField('User name', id='username',
                           validators=[DataRequired(), Length(min=2)])
    first_name = StringField('First name', id='first_name',
                             validators=[DataRequired(), Length(min=2)])
    last_name = StringField('Last name', id='last_name',
                            validators=[DataRequired(), Length(min=3)])
    password = PasswordField('Password', id='password',
                             validators=[DataRequired(), Length(min=4, max=100)])
    confirm_password = PasswordField('Confirm password', id='confirm_password',
                                     validators=[DataRequired(), Length(min=4, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    sign_up_submit = SubmitField('Sign up', id='sign_up_submit')
    profile_password = PasswordField('Password', validators=[Length(min=4, max=100)])
    profile_confirm_password = PasswordField('Password', validators=[Length(min=4, max=100)])
    profile_submit = SubmitField('Save')

    logout = BooleanField('confirm')

    logout_submit = SubmitField('Logout', id='log_out')
    upload = FileField('Upload avatar')
    upload_submit = SubmitField('Upload')
    comment = TextAreaField("Message", validators=[DataRequired()])
    comment_submit = SubmitField('Submit', id='comment_submit')

    add_game_submit = SubmitField('Add new game', id='add_new_game')
    add_game_name = StringField('Name',validators=[DataRequired()])
    add_game_description = TextAreaField("Description", validators=[DataRequired()])
    upload_game_image = FileField('Upload image')
    game_price = StringField('Price', validators=[DataRequired()])
    game_genre = StringField('Genre',validators=[DataRequired()])
    cart_add = SubmitField()
    cart_sub = SubmitField()
