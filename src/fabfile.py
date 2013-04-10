# -*- coding: utf-8 -*-
#
# Copyright (c) 2010-2012 Cidadania S. Coop. Galega
#
# This file is part of e-cidadania.
#
# e-cidadania is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# e-cidadania is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with e-cidadania. If not, see <http://www.gnu.org/licenses/>.

from fabric.api import local, settings, abort, run, cd, env
from fabric.contrib.console import confirm
from fabric.operations import put

# Commands
#
# Testing only: fab test (inside the project dir)
# Straight deploy (no testing): fab deploy:TYPE (type can be 'demo' or 'app')
# Full deploy (well tested): fab full_deploy:TYPE

env.hosts = ['188.40.90.250']


def test():
    """
    Executes all the tests of the platform and if the tests failed it will prompt
    the user to continue or not. If the tests were succesful continue.
    """
    with settings(warn_only=True):
        result = local('./manage.py test', capture=True)
    if result.failed and not confirm("Tests failed. Continue anyway?"):
        abort("Aborting at user request.")


def deploy(type):
    """
    Automate the deployment in the e-cidadania VPS. First it checks if the
    directory exists. If not, creates a new clone. If it exists, makes a pull
    and updates the code. After that it copies a local version of the production
    configuration.

    Type: demo, app
    """
    print "WARNING: Remember that this deployment is untested. For full testing\
and deployment use 'full_deploy' function\n"
    src_dir = '/home/oscarcp/deploy/ecidadania-%s/' % type
    with settings(warn_only=True):
        if run("test -d %s" % src_dir).failed:
            run("git clone git://github.com/cidadania/e-cidadania.git %s" % src_dir)
    with cd(src_dir):
        run("git pull")
        put('~/devel/conf/ecidadania/%s/settings/*' % type, 'src/e_cidadania/settings/')
        with cd('src/'):
            run('./manage.py syncdb')
            run('./manage.py collectstatic')


def full_deploy(type):
    """
    Full deploy will make all the necessary tests to guarantee that the platform
    cam be updated, and after that, it will deploy the selected version in the
    server.
    """
    test()
    deploy(type)
