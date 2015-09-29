# -*- coding:utf-8 -*-
from flask import url_for, render_template, redirect, request, Blueprint

from app import db
from forms import LoginForm
from models import User


login = Blueprint('login', __name__, template_folder='templates')


# 로그인 페이지
@login.route('/sign_in', methods=['GET'])
def sign_in():
    form = LoginForm()
    return render_template('login.html', form=form)


# 로그인 
@login.route('/sign_up', methods=['POST'])
def sign_up():
    form = LoginForm()
    if form.validate_on_submit():
        user = User()
        form.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('.sign_in'))
    return render_template('login.html', form=form)
