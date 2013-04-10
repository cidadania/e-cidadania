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


from core.spaces import url_names

from tests.test_utils import ECDTestCase


class ViewSpaceIndexTest(ECDTestCase):

    """
    Tests the view for the index page of a space.
    """
    
    def setUp(self):
        super(ViewSpaceIndexTest, self).init()
        self.admin_space=self.foo_space
        self.user_space=self.bar_space

    def testUserAccess(self):
        """
        Tests if only the allowed user can access the space index page.
        """
        #Not a public space
        self.admin_space.public = False
        self.admin_space.save()
        
        url = self.getURL(url_names.SPACE_INDEX,
                          kwargs={'space_url': self.admin_space.url})
        response = self.get(url)
        self.assertResponseOK(response)
        self.assertContains(response, "You're an anonymous user.")
        #print self.printResponse(response)
        
        user = self.login("test_user", "test_password")
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_anonymous())
        self.assertFalse(user in self.admin_space.users.all())
        self.assertFalse(user in self.admin_space.mods.all())
        self.assertFalse(user in self.admin_space.admins.all())
        response = self.get(url)
        self.assertResponseOK(response)
        self.assertContains(response, "You're not registered to this             space.")
        
        self.logout()
        
        url = self.getURL(url_names.SPACE_INDEX,
                          kwargs={'space_url': self.user_space.url})
        self.assertTrue(self.user_space.public)
        response = self.get(url)      
        #print self.printResponse(response)
        self.assertResponseOK(response)
        self.assertContains(response, "Hello anonymous user.")
        
        user.public = False
        user.is_staff = True
        user.save()
        self.assertTrue(user.is_staff)
        self.assertFalse(user.public)
        url = self.getURL(url_names.SPACE_INDEX, 
                          kwargs={'space_url': self.user_space.url})
        response = self.get(url)
        self.assertResponseOK(response)
        self.assertContains(response, "Hello anonymous user.")
        
        admin = self.login(self.admin_username, self.admin_password)
        self.assertTrue(self.isLoggedIn(admin))
#       self.assertTrue(admin.is_superuser)
        self.assertFalse(admin.is_superuser)
        response = self.get(url)
        self.assertResponseOK(response)

        superuser=self.create_super_user()
        self.login('admin','admin_pass')
        self.assertTrue(self.isLoggedIn(superuser))
        self.assertTrue(superuser.is_superuser)
        response = self.get(url)
        self.assertResponseOK(response)

        self.logout()
        response = self.get(url)
        self.assertResponseOK(response)
        self.assertContains(response, "Hello anonymous user.")
