# -*- coding:utf-8 -*-
import math
import time

from bcrypt import hashpw
from flask import jsonify, redirect, request, session, Blueprint
from sqlalchemy import and_

from app import db
from decorators import login_required
from forms import GPSForm
from models import GPS, Riding, User

api = Blueprint('api', __name__, template_folder='templates', 
                url_prefix='/api')

ONE_DEGREE = 1000. * 10000.8 / 90.


@api.route('/gps/', methods=['POST'])
def post_gps():
    distance = 0
    avg_speed = 0
    riding_id = request.values.get('riding_id')

    form = GPSForm(csrf_enabled=False)
    if form.validate_on_submit():
        gps = GPS()
        form.populate_obj(gps)
        db.session.add(gps)
        db.session.flush()

        gpses = db.session.query(GPS)\
                          .filter_by(riding_id=riding_id)\
                          .order_by(GPS.id).all()

        if gpses:
            start_time = gpses[0].timestamp
            end_time = gpses[len(gpses)-1].timestamp

            for i, g in enumerate(gpses):
                if i+1 != len(gpses):
                    first = gpses[i]
                    second = gpses[i+1]
                    coef = math.cos(float(second.latitude) / 180. * math.pi)
                    x = float(second.latitude) - float(first.latitude)
                    y = (float(second.longitude) - float(first.longitude)) * coef
                    distance += math.sqrt(x * x + y * y) * ONE_DEGREE

            avg_speed = round(float(distance / 1000) /
                        (1 if float((end_time - start_time).seconds) == 0 else 
                         float((end_time - start_time).seconds) /
                         float(3600)), 1)
            distance = round(float(distance / 1000), 1)

            riding = db.session.query(Riding).filter_by(id=riding_id)
            riding.avg_speed = avg_speed

        db.session.commit()
        return jsonify(result="success", avg_speed=avg_speed,
                       distance=distance, title=riding.title)
    return jsonify(result="fail")


@api.route('/gps/', methods=['GET'])
def get_gps():
    riding_id = request.values.get('riding_id')
    last_gps = db.session.query(GPS)\
                 .filter(GPS.riding_id == riding_id)\
                 .order_by(GPS.timestamp.desc()).first()

    if last_gps is not None:
        return jsonify(
            {c.name: getattr(last_gps, c.name)
            for c in last_gps.__table__.columns}
        )
    else:
        return jsonify(result="fail")


@api.route('/sign_in/', methods=['POST'])
def post_sign_in():
    email = request.values.get('email')
    password = request.values.get('password')
    user = db.session.query(User).filter_by(email=email).first()

    if hashpw(str(password), str(user.password)) == str(user.password):
        session['user'] = user.id
        return jsonify(result='success', user_id=user.id)
    return jsonify(result='fail')


@api.route('/sign_out/', methods=['POST'])
def post_sign_out():
    if 'user' in session:
        session.pop('user', None)
        return jsonify(result='success')
    return jsonify(result='fail')


@api.route('/riding', methods=['POST'])
def post_riding():
    riding = Riding(user_id=request.values.get('user_id'))
    db.session.add(riding)
    db.session.commit()
    return jsonify(result='success', riding_id=riding.id)

