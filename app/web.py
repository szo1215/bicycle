# -*- coding:utf-8 -*-
from datetime import datetime
import math
import redis
import time

from bcrypt import hashpw
from flask import (jsonify, redirect, render_template, request, session, 
                   url_for, Blueprint)
from sqlalchemy.sql import func

from app import db
from decorators import web_login_required
from forms import SignUpForm
from models import GPS, Riding, User

ONE_DEGREE = 1000. * 10000.8 / 90.

web = Blueprint('web', __name__, template_folder='templates')

pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
r = redis.Redis(connection_pool=pool)


def serialize(Object, attribute=[]):
    d = {}

    for key in Object.__table__.columns.keys():
        if key in attribute:
            value = Object.__getattribute__(key)
            if isinstance(value, datetime):
                value = value.strftime('%Y-%m-%d %H-%m')
            d[key] = value
    return d


@web.route('/')
@web_login_required
def index():
    return render_template('map.html', name=session['name'])


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
        session['name'] = user.name
        return redirect(url_for('web.index'))
    return redirect(url_for('web.login'))


@web.route('/logout', methods=['GET'])
def post_logout():
    if 'user' in session:
        session.pop('user', None)
    return redirect(url_for('web.index'))


@web.route('/last_riding_info', methods=['GET'])
@web_login_required
def get_last_riding_info():
    distance = 0
    avg_speed = 0
    tracking = []
    last_riding = 0

    last_riding = db.session.query(Riding.id, Riding.created_date)\
                    .join(User)\
                    .filter_by(id=session['user'])\
                    .order_by(Riding.created_date.desc())\
                    .limit(1).first()

    gpses = db.session.query(GPS)\
                      .filter_by(riding_id=last_riding.id)\
                      .order_by(GPS.id).all()
    if gpses:
        for gps in gpses:
            tracking.append([gps.latitude, gps.longitude])

        start_time = gpses[0].timestamp
        end_time = gpses[len(gpses)-1].timestamp

        for i, g in enumerate(gpses):
            if len(gpses) >= 2 and i+1 != len(gpses):
                first = gpses[i]
                second = gpses[i+1]
                coef = math.cos(second.latitude / 180. * math.pi)
                x = second.latitude - first.latitude
                y = (second.longitude - first.longitude) * coef
                distance += math.sqrt(x * x + y * y) * ONE_DEGREE
        
        avg_speed = round(float(distance / 1000) / 
                    (1 if float((end_time - start_time).seconds) == 0 else 
                     float((end_time - start_time).seconds) / float(3600)), 1)
        distance = round(float(distance / 1000), 1)

    return jsonify(tracking=tracking,
            distance=str(distance) + "km",
            avg_speed=str(avg_speed) + "km/h" ,
            last_riding_id=last_riding.id,
            last_riding_date=last_riding.created_date.strftime('%Y. %m. %d')
    )


@web.route('/friends', methods=['GET'])
@web_login_required
def get_friends():
    return jsonify(
        friends=[serialize(u, ['name']) for u in db.session.query(User).all()]
    )


@web.route('/tracking', methods=['GET'])
@web_login_required
def get_tracking():
    path = []

    last_riding = db.session.query(Riding.id)\
                    .join(User)\
                    .filter_by(id=session['user'])\
                    .order_by(Riding.created_date.desc())\
                    .limit(1)
    sub = last_riding.subquery('last')
    gps = db.session.query(GPS)\
                    .filter_by(riding_id=sub.c.id)\
                    .order_by(GPS.timestamp.desc())\
                    .first()

    path.append([gps.latitude, gps.longitude])

    return jsonify(last_riding_id=last_riding.first().id, path=path)


@web.route('/ranking', methods=['GET'])
@web_login_required
def get_ranking():
    subs = db.session.query(Riding.user_id,
                            func.max(Riding.avg_speed).label('avg_speed'))\
                     .group_by(Riding.user_id).subquery('sub')
    rankings = db.session.query(User.name, subs.c.avg_speed).join(subs).all()
    for ranking in rankings:
        r.zadd('riding_rank', ranking.name, ranking.avg_speed)
    return jsonify(scores=r.zrange('riding_rank', 0, 5, 'WITHSCORES'))
