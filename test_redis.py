import math

import redis

from app.app import db
from app.models import Riding, GPS, User

ONE_DEGREE = 1000. * 10000.8 / 90.
pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
r = redis.Redis(connection_pool=pool)

ridings = db.session.query(Riding).order_by(Riding.id.desc()).all()

for r in ridings:
    distance = 0
    total = db.session.query(GPS).filter_by(riding_id=r.id).order_by(GPS.id).all()
    start_time = total[0].timestamp
    end_time = total[len(total)-1].timestamp

    for i, g in enumerate(db.session.query(GPS).filter_by(riding_id=r.id).order_by(GPS.id.desc()).all()):
        if i+1 != len(total):
            first = total[i]
            second = total[i+1]
            coef = math.cos(second.latitude / 180. * math.pi)
            x = second.latitude - first.latitude
            y = (second.longitude - first.longitude) * coef
            distance += math.sqrt(x * x + y * y) * ONE_DEGREE

    print float(distance / 1000) / (float((end_time - start_time).seconds) / float(3600))
