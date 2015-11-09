from fabric.api import env, run

env.hosts = ['ec2-52-192-43-64.ap-northeast-1.compute.amazonaws.com']
env.user = 'ubuntu'
env.key_filename = ['Kya.pem']


def deploy():
    run('cd bicycle')
    run('. env/bin/activate')
    run('git pull upstream master')
    run('alembic upgrade head')
    run('nohup python run.py &')

