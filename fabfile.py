# -*- coding: utf-8 -*-

from datetime import date
from fabric.api import cd, run, env, local, sudo, hosts


LIVE_DIR = '/home/keyua/keyua-site'
STAGING_DIR = '/home/keyua/keyua-site'


def local_push():
    local('git push')


def local_pull():
    local('git pull')


def server_pull(dir):
    with cd(dir):
        run('git pull')


def collectstatic(dir, noinput=True):
    with cd(dir):
        run('./manage.py collectstatic {}'.format('--noinput' if noinput else ''))


def migrate(dir, app=False):
    with cd(dir):
        run('./manage.py migrate {}'.format(app if app else ''))


def update_env(dir):
    """
    Updates project environment.
    """
    with cd(dir):
        run('./build/buildenv.sh')


def supervisor_restart(app_name):
    """
    Restarts supervisor.
    """
    sudo('supervisorctl stop {}'.format(app_name))
    sudo('supervisorctl start {}'.format(app_name))


def update_logs_files(dir):
    """
    Removes and creates again log files.
    """
    dir = dir + '/logs'
    with cd(dir):
        run('rm wsgi.log')
        run('touch wsgi.log')
        # run('rm celery.log')
        # run('touch celery.log')


@hosts(['root@45.56.73.186'])
def update_live():
    """
    Updating live server.
    """
    local_pull()
    local_push()

    server_pull(LIVE_DIR)
    update_env(LIVE_DIR)
    migrate(LIVE_DIR)
    collectstatic(LIVE_DIR)

    update_logs_files(LIVE_DIR)

    supervisor_restart('keyua')
    # supervisor_restart('celery')


@hosts(['root@45.56.73.186'])
def update_live_backend():
    """
    Updating live server.
    """
    local_pull()
    local_push()

    server_pull(LIVE_DIR)
    migrate(LIVE_DIR)

    supervisor_restart('keyua')


@hosts(['root@45.56.73.186'])
def update_live_static():
    """
    Updating live server.
    """
    local_pull()
    local_push()

    server_pull(LIVE_DIR)
    update_env(LIVE_DIR)

    collectstatic(LIVE_DIR)

    # supervisor_restart('keyua')


@hosts(['root@176.58.110.40'])
def create_dump_folters(dump_date=None):
    dump_date = dump_date or str(date.today())
    with cd('/home/'):
        run('mkdir {}'.format(dump_date))


@hosts(['root@45.56.73.186'])
def save_dump():
    db_file = 'keyua.sqlite3'
    media_folder = 'media'
    dump_date = str(date.today())

    remote_folter = '/home/{}'.format(dump_date)

    with cd(LIVE_DIR):
        run('scp {} root@176.58.110.40:{}'.format(db_file, remote_folter))
        run('scp -r {} root@176.58.110.40:{}'.format(media_folder, remote_folter))


# @hosts(['keyua@72.14.190.170'])
# def update_staging():
#     """
#     Updates the Staging server with the latest changes.
#     """
#     local_pull()
#     local_push()

#     server_pull(STAGING_DIR)

#     update_logs_files(STAGING_DIR)

#     supervisor_restart('keyua_site')
#     supervisor_restart('celery')
