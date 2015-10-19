# -*- coding:utf-8 -*-
from flask import render_template, request, Blueprint

from app import db
from decorators import login_required

web = Blueprint('web', __name__, template_folder='templates')


@web.route('/')
def index():
    return render_template('map.html')
