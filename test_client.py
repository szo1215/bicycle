# -*- coding:utf-8 -*-
import gpxpy
import time

from app.app import db
from app.models import Riding, GPS, User

start_time = time.time()
gpx_file = open("test.gpx")
gpx = gpxpy.parse(gpx_file)

for user in db.session.query(User).all():
    for r in range(0, 20):
        r = Riding(user=user, title='good')
        db.session.add(r)
        time.sleep(2)
    db.session.commit()

ridings = db.session.query(Riding).all()

for r in ridings:
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                g = GPS(riding=r, 
                        latitude=point.latitude,
                        longitude=point.longitude,
                        altitude=point.elevation,
                        timestamp=point.time)
                db.session.add(g)
    db.session.commit()

print "%s seconds" % (time.time() - start_time)

