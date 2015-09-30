# -*- coding:utf-8 -*-
from functools import wraps

from flask import url_for, redirect, session


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' in session:
            return f(*args, **kwargs)
        return redirect(url_for('login.get_sign_up'))
    return decorated_function

