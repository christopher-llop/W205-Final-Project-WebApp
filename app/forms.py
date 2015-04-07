__author__ = 'cjllop'
from flask_wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired

class LoginForm(Form):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)

class PostForm(Form):
    post = StringField('post', validators=[DataRequired()])