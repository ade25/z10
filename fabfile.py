from fabric.api import cd
from fabric.api import env
from fabric.api import local
from fabric.api import run
from fabric.api import task

from ade25.fabfiles import project
from ade25.fabfiles.server import setup
from ade25.fabfiles.server import controls
from ade25.fabfiles import hotfix as hf

env.use_ssh_config = True
env.forward_agent = True
env.port = '22222'
env.user = 'root'
env.code_user = 'root'
env.prod_user = 'www'
<<<<<<< HEAD
env.webserver = 'zope10'
=======
env.webserver = '/opt/webserver/buildout.webserver'
>>>>>>> bd1315cfc9c7598acf67934ed3b895b2b261c0ab
env.code_root = '/opt/webserver/buildout.webserver'
env.host_root = '/opt/sites'

env.hosts = ['zope10']
env.hosted_sites = [
    'base',
    'gold',
    'demo',
    'renaissance',
    'wiretechnologies',
    'girocom',
    'putzteufel',
    'trainandmore',
    'viyoma',
    'zwerge',
]

env.hosted_sites_locations = [
    '/opt/sites/base/buildout.base',
    '/opt/sites/gold/buildout.gold',
    '/opt/sites/demo/buildout.demo',
    '/opt/sites/renaissance/buildout.renaissance',
    '/opt/sites/wiretechnologies/buildout.wiretechnologies',
    '/opt/sites/girocom/buildout.girocom',
    '/opt/sites/putzteufel/buildout.putzteufel',
    '/opt/sites/trainandmore/buildout.trainandmore',
    '/opt/sites/viyoma/buildout.viyoma',
    '/opt/sites/zwerge/buildout.zwerge',
]


@task
def push():
    """ Push committed local changes to git """
    local('git push')


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
<<<<<<< HEAD
=======
def nginx(*cmd):
    """Runs an arbitrary supervisorctl command."""
    with cd(env.webserver):
        run('nice bin/supervisorctl ' + ' '.join(cmd) + ' nginx')


@task
>>>>>>> bd1315cfc9c7598acf67934ed3b895b2b261c0ab
def restart_varnish():
    """ Restart Varnish """
    controls.restart_varnish()


@task
def restart_haproxy():
    """ Restart HAProxy """
    controls.restart_haproxy()


@task
<<<<<<< HEAD
def supervisorctl(*cmd):
=======
def ctl(*cmd):
>>>>>>> bd1315cfc9c7598acf67934ed3b895b2b261c0ab
    """Runs an arbitrary supervisorctl command."""
    with cd(env.webserver):
        run('nice bin/supervisorctl ' + ' '.join(cmd))


@task
def deploy():
    """ Deploy current master to production server """
    push()
    controls.update()
    controls.build()


@task
def deploy_site():
    """ Deploy a new site to production """
    push()
    controls.update()
    controls.build()
    controls.reload_supervisor()


@task
def hotfix(addon=None):
    """ Apply hotfix to all hosted sites """
    hf.prepare_sites()
    hf.process_hotfix()
