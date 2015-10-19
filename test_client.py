# -*- coding:utf-8 -*-
import gpxpy
import requests
import time

start_time = time.time()
gpx_file = open("test.gpx")
gpx = gpxpy.parse(gpx_file)

for track in gpx.tracks:
    for segment in track.segments:
        for point in segment.points:
            r = requests.post("http://localhost:5000/api/gps/", 
                              data={"latitude":point.latitude, 
                                    "longitude":point.longitude,
                                    "altitude":point.elevation,
                                    "riding_id":2})
            print r.status_code

print "%s seconds" % (time.time() - start_time)
