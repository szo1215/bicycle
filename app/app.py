# -*- coding:utf-8 -*-
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

db = SQLAlchemy(app)

app.config.from_object('config')

from api import api
from login import login
from web import web

app.register_blueprint(api)
app.register_blueprint(login)
app.register_blueprint(web)

