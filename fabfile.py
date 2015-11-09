from fabric.api import env, run

env.hosts = ['ec2-52-192-43-64.ap-northeast-1.compute.amazonaws.com']
env.user = 'ubuntu'
env.key_filename = ['Kya.pem']


def hello():
    run('ls')

