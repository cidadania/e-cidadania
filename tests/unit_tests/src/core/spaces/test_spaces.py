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
        self.private_space = self.foo_space
        self.private_space_url = self.getURL(url_names.SPACE_INDEX,
                                        kwargs={'space_url': self.private_space.url})
        self.public_space = self.bar_space
        self.public_space_url = self.getURL(url_names.SPACE_INDEX,
                                            kwargs={'space_url': self.public_space.url})
                                        
    def testAnonymousUserCanNotAccessPrivateSpace(self):
        """
        Tests if anonymous user can not access the space index page.
        """        
        response = self.get(self.private_space_url)
        self.assertResponseOK(response)
        self.assertContains(response, "You're an anonymous user.")
    
    def testUnregisteredUserCanNotAccessPrivateSpace(self):
        """Tests if an unregistered user can not access the space index.
        """
        #Create and login a user who is not registered to the space
        user = self.login("test_user", "test_password")
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_anonymous())
        self.assertFalse(user in self.private_space.users.all())
        self.assertFalse(user in self.private_space.mods.all())
        self.assertFalse(user in self.private_space.admins.all())
        response = self.get(self.private_space_url)
        self.assertResponseOK(response)
        self.assertContains(response, "You're not registered to this             space.")
        self.logout()
   
    def testSpaceAdminCanAccessThePrivateSpace(self):
        """Tests if the space admin can access the space index.
        """     
        space_admin = self.login('foo_admin', 'foo_admin_password')
        self.assertTrue(self.isLoggedIn(space_admin))
        
        response = self.get(self.private_space_url)
        self.assertResponseOK(response)
        self.assertTemplateNotUsed(response, 'not_allowed.html')
        self.logout()
    
    def testSpaceModCanAccessThePrivateSpace(self):
        """Tests if the space mod can access the space index.
        """
        space_mod = self.login('foo_mod', 'foo_mod_password')
        self.assertTrue(self.isLoggedIn(space_mod))
        response = self.get(self.private_space_url)
        self.assertResponseOK(response)
        self.assertTemplateNotUsed(response, 'not_allowed.html')
        self.logout()
    
    def testSpaceUserCanAccessTheSpace(self):
        """Tests if the space user can access the space index.
        """
        space_user =  self.login('foo_user', 'foo_user_password')
        self.assertTrue(self.isLoggedIn(space_user))
        response = self.get(self.private_space_url)
        self.assertResponseOK(response)
        self.assertTemplateNotUsed(response, 'not_allowed.html')
        self.logout()
    
    def testOtherUsersCanNotAccessThePrivateSpace(self):
        """Test if other users who are not registered to the space can not
        access the space.
        """
        other_user = self.login('bar_admin', 'bar_admin_password')
        self.assertTrue(self.isLoggedIn(other_user))
        self.assertFalse(other_user in self.private_space.admins.all())
        response = self.get(self.private_space_url)
        self.assertResponseOK(response)
        self.assertTemplateUsed(response, 'not_allowed.html')
        
  
    def testAdminAccessToAPublicSpace(self):
        """Tests if an admin for one space can access a public space.
        """
        admin = self.login('foo_admin', 'foo_admin_password')
        self.assertTrue(self.isLoggedIn(admin))
        self.assertFalse(admin in self.public_space.admins.all())
        response = self.get(self.public_space_url)
        self.assertResponseOK(response)
        self.assertTemplateNotUsed(response, 'not_allowed.html')

    def testAnonymousUserCanAcessAPublicSpace(self):
        """Tests if an anonymous user can access a public space.
        """
        response = self.get(self.public_space_url)
        self.assertResponseOK(response)
        self.assertTemplateNotUsed(response, 'not_allowed.html')
    

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
        space = self.bar_space
        general_user = self.login('test_user', 'test_password')
        url = self.getURL(url_names.SPACE_DELETE, kwargs={'space_url': space.url})
        response = self.get(url)
        self.assertResponseRedirect(response)
        self.assertEqual(url, response.request['PATH_INFO'])
    
    def testAdminAccess(self):
        """
        Tests if a correct admin can delete a space.
        """
        space =self.bar_space
        user = self.create_super_user("other_admin", "other_password",
                                      logged_in=True)
        self.assertTrue(self.isLoggedIn(user))
        
        url = self.getURL(url_names.SPACE_DELETE, kwargs={'space_url': space.url})
        response = self.get(url)
        self.assertResponseOK(response)
        self.assertTemplateUsed(response, 'not_allowed.html')
        
        #logout the present user because the space does not belong to it
        self.logout()
        admin = self.login('bar_admin', 'bar_admin_password')
        self.assertTrue(self.isLoggedIn(admin))
        self.assertTrue(admin in space.admins.all())
        response = self.get(url)
        self.assertResponseRedirect(response)
        self.assertTemplateNotUsed(response, 'not_allowed.html')

class ListSpacesTest(ECDTestCase):
    """
    Tests the list spaces view.
    """
    
    def setUp(self):
        self.init()
        #We have a public space as well as a private space.
        self.private_space = self.foo_space
        self.public_space = self.bar_space
        self.url = self.getURL(url_names.SPACE_LIST)
               
    def testOnlyPublicSpacesAreListedForAnonymousUser(self):
        """
        Tests if only the public spaces are listed for anonymous user.
        """
        #No user is logged in currently
        response = self.get(self.url)
        self.assertResponseOK(response)
        spaces_returned = response.context[0].dicts[0]['space_list']
        self.assertEqual(len(spaces_returned), 1)
        self.assertTrue(self.public_space in spaces_returned)
        self.assertTrue(self.private_space not in spaces_returned)
    
    def testAllSpacesAreReturnedForALoggedInUser(self):
        """
        Tests if both the public and private spaces are returned for a logged
        in user who is registered for both the spaces.
        
        We make self.bar_admin to be a user for self.foo_space which is a
        private space.
        """    
        self.foo_space.users.add(self.bar_admin)
        self.login('bar_admin', 'bar_admin_password')
        response = self.get(self.url)
        spaces_returned = response.context[0].dicts[0]['space_list']
        self.assertEqual(len(spaces_returned), 2)
        self.assertTrue(self.foo_space in spaces_returned)
        self.assertTrue(self.bar_space in spaces_returned)   

class EditRoleTest(ECDTestCase):
    """
        Tests if only admin can edit roles of people
    """	

    def setUp(self):
        self.init()
        self.private_space = self.foo_space
        self.public_space = self.bar_space

    def testSuperuserCanAccessPrivateView(self):
        space=self.private_space
        self.root=self.create_super_user(logged_in=True)
        self.assertTrue(self.isLoggedIn(self.root))
        url = self.getURL('edit-roles', kwargs={'space_url': space.url})
        response = self.get(url,follow=True)
        self.assertResponseOK(response)
        self.assertContains(response,"Please select the         users that will be administrators")
        self.logout()

    def testSuperuserCanAccessPrivateView(self):
        space=self.public_space
        self.root=self.create_super_user(logged_in=True)
        self.assertTrue(self.isLoggedIn(self.root))
        url = self.getURL('edit-roles', kwargs={'space_url': space.url})
        response = self.get(url,follow=True)
        self.assertResponseOK(response)
        self.assertContains(response,"Please select the         users that will be administrators")
        self.logout()

    def testAdminCannotAccessPrivateView(self):
        space = self.private_space
        self.login('foo_admin', 'foo_admin_password')
        self.assertTrue(self.isLoggedIn(self.foo_admin))
        url = self.getURL('edit-roles', kwargs={'space_url': space.url})
        response=self.get(url,follow=True)
        self.assertResponseOK(response)
        self.assertContains(response, "you don't have permissions for accessing to some area.")
        self.logout()

    def testAdminCannotAccessPublicView(self):
        space = self.public_space
        self.login('bar_admin', 'bar_admin_password')
        self.assertTrue(self.isLoggedIn(self.bar_admin))
        url = self.getURL('edit-roles', kwargs={'space_url': space.url})
        response=self.get(url,follow=True)
        self.assertResponseOK(response)
        self.assertContains(response, "you don't have permissions for accessing to some area.")
        self.logout()

    def testModCannotAccessPrivateView(self):
        space = self.private_space
        self.login('foo_mod', 'foo_mod_password')
        self.assertTrue(self.isLoggedIn(self.foo_mod))
        url = self.getURL('edit-roles', kwargs={'space_url': space.url})
        response=self.get(url,follow=True)
        self.assertResponseOK(response)
        self.assertContains(response, "you don't have permissions for accessing to some area.")
        self.logout()

    def testModCannotAccessPublicView(self):
        space = self.public_space
        self.login('bar_mod', 'bar_mod_password')
        self.assertTrue(self.isLoggedIn(self.bar_mod))
        url = self.getURL('edit-roles', kwargs={'space_url': space.url})
        response=self.get(url,follow=True)
        self.assertResponseOK(response)
        self.assertContains(response, "you don't have permissions for accessing to some area.")
        self.logout()


    def testUserCannotAccessPrivateView(self):
        space = self.private_space
        self.login('foo_user', 'foo_user_password')
        self.assertTrue(self.isLoggedIn(self.foo_user))
        url=self.getURL('edit-roles', kwargs={'space_url': space.url})
        response=self.get(url,follow=True)
        self.assertResponseOK(response)
        self.assertContains(response, "you don't have permissions for accessing to some area.")
        self.logout()

    def testUserCannotAccessPublicView(self):
        space = self.public_space
        self.login('bar_user', 'bar_user_password')
        self.assertTrue(self.isLoggedIn(self.bar_user))
        url = self.getURL('edit-roles',kwargs={'space_url': space.url})
        response=self.get(url,follow=True)
        self.assertResponseOK(response)
        self.assertContains(response, "you don't have permissions for accessing to some area.")
        self.logout()
	
    def testOtherUserCannotAccessPrivateView(self):
        space = self.private_space
        self.unreg_user = self.create_user('unreg_user', 'unreg_password')
        self.login('unreg_user', 'unreg_password')
        self.assertTrue(self.isLoggedIn(self.unreg_user))
        url = self.getURL('edit-roles', kwargs={'space_url': space.url})
        response=self.get(url,follow=True)
        self.assertResponseOK(response)
        self.assertContains(response, "you don't have permissions for accessing to some area.")
        self.logout()

    def testOtherUserCannotAccessPublicView(self):
        space = self.public_space
        self.unreg_user = self.create_user('unreg_user', 'unreg_password')
        self.login('unreg_user', 'unreg_password')
        self.assertTrue(self.isLoggedIn(self.unreg_user))
        url = self.getURL('edit-roles', kwargs={'space_url': space.url})
        response=self.get(url,follow=True)
        self.assertResponseOK(response)
        self.assertContains(response, "you don't have permissions for accessing to some area.")
        self.logout()
