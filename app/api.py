# -*- coding:utf-8 -*-
from flask import jsonify, redirect, request, Blueprint

from app import db
from models import GPS, User

api = Blueprint('api', __name__, template_folder='templates')


@api.route('/gps/', methods=['POST'])
def post_gps():
    try:
        j = json.loads(request.data)
        request.values.get('')
        # FIXME: 임시로 한개의 데이터만 받도록 수정 후에 다시 원복
        """
        for k, v in j.items():
            u = GPS(latitude=v.get('latitude'),
                    longtitude=v.get('longtitude'),
                    altitude=v.get('altitude'),
                    horizontal_accuracy=v.get('horizontalAccuracy'),
                    vertical_accuracy=v.get('verticalAccuracy'),
                    timestamp=v.get('timestamp'))
            db.session.add(u)
            db.session.commit()
        """
        gps = GPS(latitude=j.get('latitude'),
                  longtitude=j.get('longtitude'),
                  altitude=j.get('altitude'),
                  horizontal_accuracy=j.get('horizontalAccuracy'),
                  vertical_accuracy=j.get('verticalAccuracy'))
        db.session.add(gps)
        db.session.commit()
        return jsonify(result="success")
    except ValueError:
        return jsonify(result="fail")


@api.route('/gps/', methods=['GET'])
def get_gps():
    last = db.session.query(GPS).order_by(GPS.timestamp.desc()).first()
    return jsonify(
        {c.name: getattr(last, c.name) for c in last.__table__.columns}
    )

