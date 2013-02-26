#/usr/bin/env python
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

import sys
import os
import subprocess

"""
This script installs a development environment in an easy way, instead of
having to execute all the bootstrapping commands.
"""

__version__ = '0.2'
print "e-cidadania install script %s\n" % __version__

# Detect where is this file
cwd = os.path.dirname(os.path.realpath(__file__))
# Change the working dir
os.chdir(cwd)

# Execute the bootstrap
print " * Bootstrapping..."
a = subprocess.Popen('python bootstrap.py', shell=True)
subprocess.Popen.wait(a)

print " * Making buildout..."
b = subprocess.Popen('bin/buildout')
subprocess.Popen.wait(b)

d = raw_input(' * Do you want to create the database? (y/n) ')

if d == 'y':
	os.chdir(cwd + '/src/')
	c = subprocess.Popen('../bin/django syncdb', shell=True)
	subprocess.Popen.wait(c)
	sys.exit(0)
elif d == 'n':
	print 'Process finished'
	print """You should follow this instructions blablabla"""
	sys.exit(0)
else:
	sys.exit(0)
