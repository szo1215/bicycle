from fabric.contrib.files import exists
from fabric.context_managers import cd
from fabric.operations import run, sudo
from fabric.state import env

env.user = 'ubuntu'
env.key_filename = ['Kya.pem']
env.hosts = ['ec2-52-192-43-64.ap-northeast-1.compute.amazonaws.com']
env.home = '/home/' + env.user
env.project_name = 'bicycle'
env.project_path = env.home + '/' + env.project_name
env.static_path = env.project_path + '/static'


def deploy():
    if exists(env.project_path):
        with cd(env.project_path):
            run('. env/bin/activate')
            sudo('pip install -e .')
            run('git pull upstream master')
            run('alembic upgrade head')

