# -*- coding:utf-8 -*-
from flask import jsonify, redirect, request, Blueprint

from app import db
from forms import GPSForm
from models import GPS, User

api = Blueprint('api', __name__, template_folder='templates')


@api.route('/gps/', methods=['POST'])
def post_gps():
    form = GPSForm()
    if form.validate_on_submit():
        gps = GPS()
        form.populate_obj(gps)
        db.session.add(gps)
        db.session.commit()
        return jsonify(result="success")
    return jsonify(result="fail")
    

@api.route('/gps/', methods=['GET'])
def get_gps():
    last = db.session.query(GPS).order_by(GPS.timestamp.desc()).first()
    return jsonify(
        {c.name: getattr(last, c.name) for c in last.__table__.columns}
    )

