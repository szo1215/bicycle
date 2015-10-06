# -*- coding:utf-8 -*-
from flask import jsonify, redirect, request, Blueprint
from sqlalchemy import and_

from app import db
from decorators import login_required
from forms import GPSForm
from models import GPS, User

api = Blueprint('api', __name__, template_folder='templates', 
                url_prefix='/api')


@api.route('/gps/', methods=['POST'])
@login_required
def post_gps():
    form = GPSForm(csrf_enabled=False)
    if form.validate_on_submit():
        gps = GPS()
        form.populate_obj(gps)
        db.session.add(gps)
        db.session.commit()
        return jsonify(result="success")
    return jsonify(result="fail")
    

@api.route('/gps/', methods=['GET'])
@login_required
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
    login = db.session.query(User).filter_by(and_(email=email,
                                                  password=password)).first()
    if login is not None:
        session['user'] = login.id
        return jsonify(result='success', user_id=login.id)
    return jsonify(result='fail')


@api.route('/sign_out/', methods=['POST'])
@login_required
def post_sign_out():
    if 'user' in session:
        session.pop('user', None)
        return jsonify(result='success')
    return jsonify(result='fail')


@api.route('/riding', methods=['POST'])
@login_required
def post_riding():
    riding = Riding(user_id=session['user'])
    db.session.add(riding)
    db.session.commit()
    return jsonify(result='success', riding_id=riding.id)

