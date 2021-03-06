# -*- coding:utf-8 -*-
from flask import url_for, render_template, redirect, request, Blueprint

from app import db
from forms import SignUpForm
from models import User


login = Blueprint('login', __name__, template_folder='templates')


# 회원가입 페이지
@login.route('/sign_up', methods=['GET'])
def get_sign_up():
    form = SignUpForm()
    return render_template('sign_up.html', form=form)


# 회원가입
@login.route('/sign_up', methods=['POST'])
def post_sign_up():
    form = SignUpForm()
    if form.validate_on_submit():
        user = User()
        form.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('.get_sign_up'))
    return render_template('sign_up.html', form=form)
