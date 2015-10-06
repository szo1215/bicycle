# -*- coding:utf-8 -*-
from bcrypt import gensalt, hashpw
from flask_wtf import Form
from wtforms.fields import DecimalField, TextField, PasswordField
from wtforms.validators import Email, Length


# 패스워드 암호화
class EncryptPasswordField(PasswordField):
    password = None

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = hashpw(valuelist[0].encode('utf-8'), gensalt())
            self.password = valuelist[0].encode('utf-8')

    def pre_validate(self, form):
        if self.password < 10 or self.password > 15:
            return False
        return hashpw(self.password, self.data) == self.data
 

# 기본적인 LoginForm
class LoginForm(Form):
    email = TextField(u'이메일', [Email(message='이메일 형식이 아닙니다.')])
    name = TextField(u'이름', [Length(max=10)])
    password = EncryptPasswordField(u'비밀번호')


# GPS Form
class GPSForm(Form):
    latitude = DecimalField(label=u'위도', places=8)
    longtitude = DecimalField(label=u'경도', places=8)
    altitude = DecimalField(label=u'고도', places=8)
    horizontal_accuracy = DecimalField(label=u'수평 정확도', places=8)
    vertical_accuracy = DecimalField(label=u'수직 정확도', places=8)

