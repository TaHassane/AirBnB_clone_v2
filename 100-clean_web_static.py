#!/usr/bin/python3
"""
Task 100 Fabric script (based on the file 3-deploy_web_static.py)
that deletes out-of-date archives, using the function do_clean
deploy
"""

from fabric.api import *
from datetime import datetime
from os.path import isfile

env.user = 'ubuntu'
env.hosts = ['54.237.5.225', '	100.27.13.99']

def do_pack():
    """ Generate a .tgz archive from the contents of the web_static folder """
    time = datetime.now()
    name = 'web_static_' + str(time.year) + str(time.month) + str(time.day)
    name = name + str(time.hour) + str(time.minute) + str(time.second) + '.tgz'
    local('mkdir -p versions')
    archive = local('tar -cvzf versions/{} web_static'.format(name))
    if archive.failed:
        return None
    return 'versions/{}'.format(name)


def do_deploy(archive_path):
    """ Distribute an archive to the web servers """
    if not isfile(archive_path):
        return False
    put(archive_path, '/tmp/')
    archive = archive_path.replace('.tgz', '')
OAOAOA    archive = archive.replace('versions/', '')
OAOAOA    run('mkdir -p /data/web_static/releases/{}/'.format(archive))
    run('tar -xzf /tmp/{}.tgz -C /data/web_static/releases/{}/'
OAOAOA        .format(archive, archive))
OAOAOA    run('rm /tmp/{}.tgz'.format(archive))
    run('mv /data/web_static/releases/{}/web_static/* '.format(archive) +
        '/data/web_static/releases/{}/'.format(archive))
    run('rm -rf /data/web_static/releases/{}/web_static'.format(archive))
OAOAOA    run('rm -rf /data/web_static/current')
    run('ln -s /data/web_static/releases/{}/ /data/web_static/current'
        .format(archive))
    print('New version deployed!')
    return True


OAOAOAdef deploy():
    """ Create and distribute an archive to the web servers """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)


def do_clean(number=0):
    """ Deletes out-of-date archives """

    try:
        number = int(number)
    except:
        return None

    if number < 0:
OAOAOA        return None
OAOAOA
OAOAOA    number = 2 if (number == 0 or number == 1) else (number + 1)
OAOAOA
    with lcd("./versions"):
        local('ls -t | tail -n +{:d} | xargs rm -rf --'.
              format(number))

    with cd("/data/web_static/releases"):
        run('ls -t | tail -n +{:d} | xargs rm -rf --'.
            format(number))
