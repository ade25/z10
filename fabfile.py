from fabric.api import cd
from fabric.api import env
from fabric.api import local
from fabric.api import run
from fabric.api import task

from ade25.fabfiles import project
from ade25.fabfiles.server import setup
from ade25.fabfiles.server import status
from ade25.fabfiles.server import controls
from ade25.fabfiles import hotfix as hf

env.use_ssh_config = True
env.forward_agent = True
env.port = '22222'
env.user = 'root'
env.code_user = 'root'
env.prod_user = 'www'
env.webserver = 'zope10'
env.code_root = 'zope10'
env.host_root = '/opt/sites'

env.hosts = ['zope10']
env.hosted_sites = [
    'example.tld',
]

env.hosted_sites_locations = [
    '/opt/sites/example.tld/buildout.example.tld',
]


@task
def restart():
    """ Restart all """
    with cd(env.webserver):
        run('nice bin/supervisorctl restart all')


@task
def restart_nginx():
    """ Restart Nginx """
    controls.restart_nginx()


@task
def restart_varnish():
    """ Restart Varnish """
    controls.restart_varnish()


@task
def restart_haproxy():
    """ Restart HAProxy """
    controls.restart_haproxy()


@task
def supervisorctl(*cmd):
    """Runs an arbitrary supervisorctl command."""
    with cd(env.webserver):
        run('nice bin/supervisorctl ' + ' '.join(cmd))


@task
def prepare_deploy():
    """ Push committed local changes to git """
    local('git push')


@task
def deploy():
    """ Deploy current master to production server """
    project.site.update()
    project.site.build()
    with cd(env.webserver):
        run('bin/supervisorctl reread')
        run('bin/supervisorctl update')


@task
def hotfix(addon=None):
    """ Apply hotfix to all hosted sites """
    hf.prepare_sites()
    hf.process_hotfix()


@task
def setup_python():
    with cd('/opt'):
        setup.install_python()


def initialize_server():
    """ Initialize new server (should normally only run once) """
    setup.install_system_libs()
    setup.set_project_user_and_group('www', 'www')
    setup.configure_egg_cache
    with cd('/opt'):
        setup.install_python()
