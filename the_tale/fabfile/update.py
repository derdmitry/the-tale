# coding: utf-8

from fabric.api import task, run, env, cd, prefix

from fabfile.utils import close_to_503, stop_workers
from fabfile.backup import backup_project

from meta_config import meta_config

env.hosts = ['the-tale@the-tale.org']


@task
def update():

    with close_to_503(), stop_workers():
        backup_project()
        update_project()
    

def update_project():
    
    with prefix('. /home/the-tale/env/bin/activate'):
        run('pip install --upgrade "git+git://github.com/Tiendil/dext.git#egg=Dext" -r https://raw.github.com/Tiendil/dext/master/requirements.txt')
        run('pip install --upgrade git+git://github.com/Tiendil/pynames.git#egg=Pynames')
        run('pip install --upgrade git+ssh://git@github.com/Tiendil/the-tale.git#egg=TheTale')

    run('ln -s /home/the-tale/env/lib/python2.7/site-packages/the_tale /home/the-tale/project')
    run('ln -s /home/the-tale/conf/settings_local.py  /home/the-tale/project/settings_local.py')
    run('ln -s /home/the-tale/env/lib/python2.7/site-packages/django/contrib/admin/media /home/the-tale/project/static/admin')
    run('ln -s /home/the-tale/env/lib/python2.7/site-packages/the_tale/static /home/the-tale/static/%s' % meta_config.static_data_version)

    with cd('/home/the-tale/project'):

        run('chmod +x ./manage.py')

        with prefix('. /home/the-tale/env/bin/activate'):
            run('./manage.py syncdb')
            run('./manage.py migrate')
            run('./manage.py portal_postupdate_operations')
            run('./manage.py map_update_map')
