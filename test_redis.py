import math
import random
import time

import redis

from app.app import db
from app.models import Riding, RidingRank, GPS, User

ONE_DEGREE = 1000. * 10000.8 / 90.
pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
r = redis.Redis(connection_pool=pool)

ridings = db.session.query(Riding).order_by(Riding.id.desc()).all()

# DB
"""
for riding in ridings:
    distance = 0
    total = db.session.query(GPS).filter_by(riding_id=riding.id).order_by(GPS.id).all()
    start_time = total[0].timestamp
    end_time = total[len(total)-1].timestamp

    for i, g in enumerate(db.session.query(GPS).filter_by(riding_id=riding.id).order_by(GPS.id.desc()).all()):
        if i+1 != len(total):
            first = total[i]
            second = total[i+1]
            coef = math.cos(second.latitude / 180. * math.pi)
            x = second.latitude - first.latitude
            y = (second.longitude - first.longitude) * coef
            distance += math.sqrt(x * x + y * y) * ONE_DEGREE

    avg_speed = float(distance / 1000) / (float((end_time - start_time).seconds) / float(3600))
    riding_rank = RidingRank(riding_id=riding.id, avg_speed=avg_speed)
    db.session.add(riding_rank)
    db.session.commit()

    ranks = db.session.query(RidingRank).order_by(RidingRank.avg_speed.desc()).limit(5).offset(0).all()

db_start_time = time.time()
ranks = db.session.query(RidingRank).order_by(RidingRank.avg_speed.desc()).limit(5).offset(0).all()
print "db time check {0}".format(time.time() - db_start_time)

db.session.query(RidingRank).delete()
db.session.commit()


# Redis
for riding in ridings:
    distance = 0
    total = db.session.query(GPS).filter_by(riding_id=riding.id).order_by(GPS.id).all()
    start_time = total[0].timestamp
    end_time = total[len(total)-1].timestamp

    for i, g in enumerate(db.session.query(GPS).filter_by(riding_id=riding.id).order_by(GPS.id.desc()).all()):
        if i+1 != len(total):
            first = total[i]
            second = total[i+1]
            coef = math.cos(second.latitude / 180. * math.pi)
            x = second.latitude - first.latitude
            y = (second.longitude - first.longitude) * coef
            distance += math.sqrt(x * x + y * y) * ONE_DEGREE

    avg_speed = float(distance / 1000) / (float((end_time - start_time).seconds) / float(3600))
    r.zadd('riding_rank', riding.id, avg_speed)

redis_start_time = time.time()
r.zrange('riding_rank', 0, 5)
print "redis time check {0}".format(time.time() - redis_start_time)
"""

for i in range(1, 100000):
    riding_rank = RidingRank(riding_id=i, avg_speed=random.randrange(10, 30))
    db.session.add(riding_rank)
db.session.commit()

for i in range(1, 100000):
    r.zadd('riding_rank', i, random.randrange(10, 30))

db_start_time = time.time()
ranks = db.session.query(RidingRank).order_by(RidingRank.avg_speed.desc()).limit(5).offset(0).all()
print "db time check {0}".format(time.time() - db_start_time)

redis_start_time = time.time()
r.zrange('riding_rank', 0, 5)
print "redis time check {0}".format(time.time() - redis_start_time)

