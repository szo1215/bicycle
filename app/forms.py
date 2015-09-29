# -*- coding:utf-8 -*-

from flask_wtf import Form
from wtforms.fields import TextField, PasswordField
from wtforms.validators import Email, Length


# 기본적인 LoginForm
class LoginForm(Form):
    email = TextField(u'이메일', [Email(message='이메일 형식이 아닙니다.')])
    name = TextField(u'이름', [Length(max=10)])
    password = PasswordField(u'비밀번호', [Length(min=10, max=15)])
