# -*- coding:utf-8 -*-
from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import backref, relationship
from sqlalchemy.schema import ForeignKey
from sqlalchemy.sql.functions import now
from sqlalchemy.types import DateTime

from app import db


class User(db.Model):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    email = Column(String(255))
    name = Column(String(255))
    password = Column(String(255))
    created_date = Column(DateTime(timezone=True),
                          nullable=False, default=now(), index=True)
    ridings = relationship('Riding', backref='user')


class Riding(db.Model):
    __tablename__ = 'riding'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    title = Column(String(255))
    created_date = Column(DateTime(timezone=True),
                          nullable=False, default=now(), index=True)
    gpses = relationship('GPS', backref='riding')


class GPS(db.Model):
    __tablename__ = 'gps'

    id = Column(Integer, primary_key=True)
    riding_id = Column(Integer, ForeignKey('riding.id'))
    latitude = Column(Float)
    longtitude = Column(Float)
    altitude = Column(Float)
    horizontal_accuracy = Column(Float)
    vertical_accuracy = Column(Float)
    timestamp = Column(DateTime(timezone=True),
                       nullable=False, default=now(), index=True)
