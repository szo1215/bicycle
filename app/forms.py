# -*- coding:utf-8 -*-

from flask_wtf import Form
from wtforms.fields import DecimalField, TextField, PasswordField
from wtforms.validators import Email, Length


# 기본적인 LoginForm
class LoginForm(Form):
    email = TextField(u'이메일', [Email(message='이메일 형식이 아닙니다.')])
    name = TextField(u'이름', [Length(max=10)])
    password = PasswordField(u'비밀번호', [Length(min=10, max=15)])


# GPS Form
class GPSForm(Form):
    latitude = DecimalField(label=u'위도', places=8)
    longtitude = DecimalField(label=u'경도', places=8)
    altitude = DecimalField(label=u'고도', places=8)
    horizontal_accuracy = DecimalField(label=u'수평 정확도', places=8)
    vertical_accuracy = DecimalField(label=u'수직 정확도', places=8)

