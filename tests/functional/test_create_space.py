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

import os

from selenium.webdriver.common.keys import Keys

from tests.functional_utils import FunctionalTestCase


class CreateSpaceTest(FunctionalTestCase):
    """Tests if the page to create a space works correctly.
    """
    
    def setUp(self):
        self.init()
        
    def testCreateSpace(self):
        username = 'test_user'
        password = 'test_password'
        self.create_super_user(username, password)
        
        url = self.live_server_url + self.getURL('site-index')
        self.browser.get(url)
        self.wait(2)
        self.browser.find_element_by_link_text("Login").click()
        self.wait(2)
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys(username)
        
        password_field  = self.browser.find_element_by_name('password')
        password_field.send_keys(password)
        self.wait(2)
        password_field.send_keys(Keys.RETURN)
        #self.wait(1)
        self.wait(2)
        
        url = self.live_server_url + self.getURL('create-space')
        self.browser.get(url)
        self.wait(2)
        
        #Now we fill the creat space form
        
        name_field = self.browser.find_element_by_name('name')
        name_field.send_keys('test_space')
        
        url_field = self.browser.find_element_by_name('url')
        url_field.send_keys('test_url')
        
        logo_field = self.browser.find_element_by_name('logo')
        logo_field.send_keys(os.getcwd()+'/generic.jpeg')
        
        banner_field = self.browser.find_element_by_name('banner')
        banner_field.send_keys(os.getcwd()+'/generic.jpeg')
        self.wait(2)
        #url_field.send_keys(Keys.RETURN)
        banner_field.submit()
        self.wait(300)