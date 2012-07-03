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

from selenium.webdriver.common.keys import Keys

from tests.functional_utils import FunctionalTestCase



class LoginPageTest(FunctionalTestCase):
    """Tests if user can log into ecidadania.
    """
    
    def setUp(self):
        self.init()
        
    def testIfAUserCanLogin(self):
        
        url = self.live_server_url + self.getURL('site-index')
        self.browser.get(url)
        #self.wait(2)
        
        self.browser.find_element_by_link_text("Login").click()
        self.wait(2)
        
        self.create_user('praveen', 'something')
        
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('praveen')
        
        password_field  = self.browser.find_element_by_name('password')
        password_field.send_keys('something')
        self.wait(2)
        password_field.send_keys(Keys.RETURN)
        self.wait(1)
        