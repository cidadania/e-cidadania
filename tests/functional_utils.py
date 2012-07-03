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

import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from django.test import LiveServerTestCase

from tests.test_utils import ECDTestCase



class FunctionalTestCase(ECDTestCase, LiveServerTestCase):
    """
    Class which provides functional testing capabilities. It subclasses both
    our custom ECDTestCase and django's LiveServerTestCase. LiveServerTestCase
    was introduced in Django 1.4 to support functional testing.
    """
    
    def init(self):
        ECDTestCase.init(self)
        self.browser = webdriver.Firefox()
        
    def setUp(self):
        """
        Setup done prior to a test run.
        """
        self.init()
        
    def tearDown(self):
        """
        Actions taken after a test run.
        """ 
        self.browser.quit()
        
    def wait(self, sec):
        """
        Halts script execution for `sec` seconds. 
        
        This is necessary because the script executes faster than the browser.
        """
        time.sleep(sec)
        return

    def login(self, browser, username='test_user', password='test_password'):
        """
        Logs into e-cidadania.
        """
        username_field = browser.find_element_by_name('username')
        username_field.send_keys(username)
        
        password_field  = browser.find_element_by_name('password')
        password_field.send_keys(password)
        self.wait(2)
        password_field.send_keys(Keys.RETURN)
