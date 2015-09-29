# -*- coding:utf-8 -*-
from setuptools import setup


install_requires = [
    'flask==0.10.1',
    'sqlalchemy==1.0.0',
    'flask-sqlalchemy==0.16',
    'gunicorn==19.3.0',
    'alembic==0.7.6',
    'psycopg2==2.5',
    'WTForms==2.0.2',
    'Flask-WTF==0.12',
]


setup(
    name='bicycle',
    version='0.1',
    install_requires = install_requires,
)
