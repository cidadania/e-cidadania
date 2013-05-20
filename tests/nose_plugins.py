# -*- coding: utf-8 -*-
#
# Copyright (c) 2010-2013 Cidadania S. Coop. Galega
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

from nose.plugins import Plugin

from django.core import management


def flush_database():
    """Flushes the default test database.
    """
    management.call_command('flush', verbosity=0, interactive=False)
                            

class DatabaseFlushPlugin(Plugin):
    """Nose plugin to flush the database after every test.
    
    The instances of models generated in one test may cause other tests to fail.
    So it is necessary to clear the test database after every test.
    """
    
    name = 'DatabaseFlushPlugin'
    enabled = True
    
    def options(self, parser, env):
        return Plugin.options(self, parser, env)
    
    def configure(self, parser, env):
        Plugin.configure(self, parser, env)
        self.enabled = True
    
    def afterTest(self, test):
        flush_database()
