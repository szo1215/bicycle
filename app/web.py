# -*- coding:utf-8 -*-
from bcrypt import hashpw
from flask import (redirect, render_template, request, session, url_for,
                   Blueprint)

from app import db
from decorators import login_required
from forms import SignUpForm
from models import User

web = Blueprint('web', __name__, template_folder='templates')


@web.route('/')
@login_required
def index():
    return render_template('map.html')


@web.route('/login', methods=['GET'])
def get_login():
    if 'user' not in session:
        form = SignUpForm()
        return render_template('sign_in.html', form=form)
    return redirect(url_for('web.index'))


@web.route('/login', methods=['POST'])
def post_login():
    email = request.values.get('email')
    password = request.values.get('password')
    user = db.session.query(User).filter_by(email=email).first()

    if hashpw(str(password), str(user.password)) == str(user.password):
        session['user'] = user.id
        return redirect(url_for('web.index'))
    return redirect(url_for('web.login'))


@web.route('/logout', methods=['GET'])
def post_logout():
    if 'user' in session:
        session.pop('user', None)
    return redirect(url_for('.index'))

