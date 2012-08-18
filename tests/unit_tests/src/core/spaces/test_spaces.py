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
from core.spaces.models import Space

from tests.test_utils import ECDTestCase


class ViewSpaceIndexTest(ECDTestCase):

    """
    Tests the view for the index page of a space.
    """
    
    def setUp(self):
        super(ViewSpaceIndexTest, self).init()
    
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
   
    def testAStaffCanAccessAPublicSpace(self):
        """Tests if a user who is a staff can access a public space.
        """
        user = self.login("test_user", "test_password")
        #self.logout()     
        user.public = False
        user.is_staff = True
        user.save()
        self.assertTrue(self.isLoggedIn(user))
        self.assertTrue(user.is_staff)
        self.assertFalse(user.public)
        url = self.getURL(url_names.SPACE_INDEX, 
                          kwargs={'space_url': self.user_space.url})
        response = self.get(url)
        self.assertResponseOK(response)
        self.assertContains(response, "Hello anonymous user.")
    
    def testAdminCanAccessAPublicSpace(self):
        """Tests if an admin can access a public space.
        """   
        admin = self.login("some_admin", "pass")
        #self.logout()
        url = self.getURL(url_names.SPACE_INDEX, 
                          kwargs={'space_url': self.user_space.url})
        self.assertTrue(self.admin.is_superuser)
        self.assertTrue(self.user_space.public)
        
        response = self.get(url)
        self.assertResponseOK(response)
        self.assertContains(response, "Hello anonymous user.")


        
class TestCreateSpace(ECDTestCase):
    """
    Tests if a space can be created successfully.
    """       
    
    def setUp(self):
        """
        Do some necessary setup before every test run.
        """        
        self.init()
    
    def testAnAdminCanAccessTheSpaceCreationPage(self):
        """
        Tests if an admin can access the page to create a space.
        """
        #Log in an admin.
        admin = self.login(self.admin_username, self.admin_password)
        
        #Check if the admin is logged in and is a superuser.
        self.assertTrue(self.isLoggedIn(admin))
        self.assertTrue(admin.is_superuser)
        
        #Get the URL for creating space.
        url = self.getURL(url_names.CREATE_SPACE)
        
        #Make a GET request to the above url.
        response = self.get(url)
        
        #Check if the response was OK.
        self.assertResponseOK(response)
        
        #Check if the correct template was used to render the response.
        self.assertTemplateUsed(response, 'spaces/space_form.html')
        
        #Check if the response was for a GET request.
        self.assertEqual(response.request['REQUEST_METHOD'], 'GET')
    

class DeleteSpaceTest(ECDTestCase):
    """
    Tests the deletion of a space.
    """
    
    def setUp(self):
        self.init()
    
    def testGeneralUserAccess(self):
        """
        Tests if a general user is prohibited from deleting the space.
        """
        space = self.admin_space
        general_user = self.login('test_user', 'test_password')
        url = self.getURL(url_names.DELETE_SPACE, kwargs={'space_url': space.url})
        response = self.get(url)
        self.assertResponseRedirect(response)
        self.assertEqual(url, response.request['PATH_INFO'])
    
    def testAdminAccess(self):
        """
        Tests if a correct admin can delete a space.
        """
        space =self.admin_space
        user = self.create_super_user("other_admin", "other_password",
                                      logged_in=True)
        self.assertTrue(self.isLoggedIn(user))
        
        url = self.getURL(url_names.DELETE_SPACE, kwargs={'space_url': space.url})
        response = self.get(url)
        self.assertResponseOK(response)
        self.assertTemplateUsed(response, 'not_allowed.html')
        
        #logout the present super user because the space does not belong to it
        self.logout()
        admin = self.login(self.admin_username, self.admin_password)
        self.assertTrue(self.isLoggedIn(admin))
        self.assertTrue(admin in space.admins.all())
        response = self.get(url)
        self.assertResponseOK(response)
        self.assertTemplateNotUsed(response, 'not_allowed.html')


class ListSpacesTest(ECDTestCase):
    """
    Tests the list spaces view.
    """
    
    def setUp(self):
        self.init()
        
        #We have two public spaces namely self.user_space and self.admin_space.
        #We create one more private space and test if this is not listed for
        #a user who does not own this space.
        space_properties = {'author': self.admin, 'public': False, 
                            'name': 'foo_space', 'url': 'foo_space_url',}
        self.private_space = self.seed(Space, properties=space_properties)
        self.assertFalse(self.private_space.public)
        
        self.url = self.getURL(url_names.LIST_SPACES)
               
    def testOnlyPublicSpacesAreListedForAnonymousUser(self):
        """
        Tests if only the public spaces are listed for anonymous user.
        """
        #No user is logged in currently
        response = self.get(self.url)
        self.assertResponseOK(response)
        spaces_returned = response.context[0].dicts[0]['space_list']
        self.assertEqual(len(spaces_returned), 2)
        self.assertTrue(self.user_space in spaces_returned)
        self.assertTrue(self.admin_space in spaces_returned)
        self.assertTrue(self.private_space not in spaces_returned)
    
    def testAllSpacesAreReturnedForALoggedInUser(self):
        """
        Tests if both the public and private spaces are returned for a logged
        in user.
        """    
        
        admin = self.login(self.admin_username, self.admin_password)
        response = self.get(self.url)
        spaces_returned = response.context[0].dicts[0]['spaces_list']
        self.assertEqual(len(spaces_returned), 3)
        self.assertTrue(self.user_space in spaces_returned)
        self.assertTrue(self.admin_space in spaces_returned)
        self.assertTrue(self.private_space in spaces_returned)        
