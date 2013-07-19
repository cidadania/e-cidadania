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

from src.core.spaces.models import Space
from src.apps.ecidadania.debate.models import Debate

from django.contrib.auth.models import *
from tests.test_utils import ECDTestCase
from django.contrib.auth.models import Group, Permission
from src.apps.ecidadania.debate import url_names as urln


class ListDebatesViewsTest(ECDTestCase):
    """Tests the views of debate app.
    """
    
    def setUp(self):
        self.init()
    
            
    def testListDebatesView(self):
        """Tests ListDebates view.
        """
        user = self.create_user('test_user', 'abcde')
        other_user = self.create_user('other_test_user', 'acsrsd')
        space_properties = {'name': 'test_space', 'url': 'test_space_url',
                            'author': user, 'public': True}
        space1 = self.seed(Space, properties=space_properties)
        
        space_properties.update({'name': 'other_space', 'url': 'other_test_url',
                                'author': other_user, 'public': True})
        space2 = self.seed(Space, space_properties)
        
        debate_properties = {'space': space1, 'author': user}
        debate1 = self.seed(Debate, properties=debate_properties)
        debate2 = self.seed(Debate, properties=debate_properties)
        debates_list = [debate1, debate2]
        
        debate_properties.update({'space': space2, 'author': other_user})
        debate3 = self.seed(Debate, properties=debate_properties)
        debate4 = self.seed(Debate, properties=debate_properties)
        debate5 = self.seed(Debate, properties=debate_properties)
        other_debates_list = [debate3, debate4, debate5]
        url = self.getURL(urln.DEBATE_LIST, kwargs={'space_url':space1.url})
        response = self.get(url)
        #print self.printResponse(response)
        self.assertResponseOK(response)
        self.assertEqual(len(response.context[0].dicts[0]['debate_list']), 
                         len(debates_list))
        
        url = self.getURL(urln.DEBATE_LIST, kwargs={'space_url': space2.url})
        response = self.get(url)
        self.assertResponseOK(response)
        self.assertEqual(len(response.context[0].dicts[0]['debate_list']), 
                         len(other_debates_list))
        
    def testViewDebate(self):
        """Tests ViewDebate view.
        """
        url = self.getURL(urln.DEBATE_VIEW,(), {'debate_id': self.foo_debate.id,
                                             'space_url': self.foo_space.url})
        response = self.get(url)
        self.assertResponseOK(response)
        context = response.context[0].dicts[0]
        assert 'notes' in context
        assert 'columns' in context
        assert 'rows' in context
        assert 'get_place' in context
        #print context['columns']
        self.assertEqual(len(context['notes']), 1)
        self.assertEqual(len(context['columns']), 1)
        self.assertEqual(len(context['rows']), 1)
        
        url = self.getURL(urln.DEBATE_VIEW,(), {'debate_id': 5,
                                             'space_url': self.foo_space.url})
        response = self.get(url)
        self.assertResponseNotFound(response)


    def testDeleteDebate(self):
        """
        Check if admin can delete from private space
        """

    
        space=self.foo_space
        self.login('foo_admin', 'foo_admin_password')
        self.foo_admin.user_permissions.add(Permission.objects.get(codename='delete_debate'))
        self.foo_admin.save()
        space.save()
        self.assertTrue(self.isLoggedIn(self.foo_admin))
        url = self.getURL(urln.DEBATE_DELETE,(), {'debate_id': self.foo_debate.id,
                                             'space_url': space.url})
        response = self.get(url)
        self.assertResponseOK(response)
        self.assertTemplateNotUsed(response, 'not_allowed.html')
        """
        When the admin doesn't have delete_debate permissions
        """
        self.foo_admin.user_permissions.remove(Permission.objects.get(codename='delete_debate'))
        self.foo_admin.save()
        space.save()
        response = self.get(url)
        self.assertResponseOK(response)
        self.assertTemplateUsed(response, 'not_allowed.html')
        self.logout()


        """
        Check if admin can delete from public space
        """


        space = self.bar_space
        self.login('bar_admin','bar_admin_password')
        self.bar_admin.user_permissions.add(Permission.objects.get(codename='delete_debate'))
        self.bar_admin.save()
        space.save()
        self.assertTrue(self.isLoggedIn(self.bar_admin))
        url = self.getURL(urln.DEBATE_DELETE,(), {'debate_id': self.bar_debate.id,
                                             'space_url': space.url})
        response = self.get(url)
        self.assertResponseOK(response)
        self.assertTemplateNotUsed(response, 'not_allowed.html')
        """
        When the admin doesn't have debate_delete permissions
        """
        self.bar_admin.user_permissions.remove(Permission.objects.get(codename='delete_debate'))
        self.bar_admin.save()
        space.save()
        response = self.get(url)
        self.assertResponseOK(response)
        self.assertTemplateUsed(response, 'not_allowed.html')
        self.logout()


        """
        Check if registered user cannot delete from private space
        """


        space = self.foo_space
        self.login('foo_user', 'foo_user_password')
        self.assertTrue(self.isLoggedIn(self.foo_user))
        self.foo_user.user_permissions.add(Permission.objects.get(codename='delete_debate'))
        self.foo_user.save()
        space.save()
        url = self.getURL(urln.DEBATE_DELETE,(), {'debate_id': self.foo_debate.id,
                                             'space_url': space.url})
        response = self.get(url)
        self.assertResponseOK(response)
        self.assertTemplateUsed(response, 'not_allowed.html')
        """
        When the user doesn't have debate_delete permissions
        """
        self.foo_user.user_permissions.remove(Permission.objects.get(codename='delete_debate'))
        self.foo_user.save()
        space.save()
        response = self.get(url)
        self.assertResponseOK(response)
        self.assertTemplateUsed(response, 'not_allowed.html')
        self.logout()


        """
        Check if registered user cannot delete from public space
        """
        space = self.bar_space
        self.login('bar_user', 'bar_user_password')
        self.assertTrue(self.isLoggedIn(self.bar_user))
        self.bar_user.user_permissions.add(Permission.objects.get(codename='delete_debate'))
        self.bar_user.save()
        space.save()
        url = self.getURL(urln.DEBATE_DELETE,(), {'debate_id': self.bar_debate.id,
                                             'space_url': space.url})
        response = self.get(url)
        self.assertResponseOK(response)
        self.assertTemplateUsed(response, 'not_allowed.html')
        """
        When the user doesn't have delete_debate permissions
        """
        self.bar_user.user_permissions.remove(Permission.objects.get(codename='delete_debate'))
        self.bar_user.save()
        space.save()
        response=self.get(url)
        self.assertResponseOK(response)
        self.assertTemplateUsed('not_allowed.html')
        self.logout()


        """
        Check if mods can delete from private space
        """


        space = self.foo_space
        self.login('foo_mod', 'foo_mod_password')
        self.assertTrue(self.isLoggedIn(self.foo_mod))
        self.foo_mod.user_permissions.add(Permission.objects.get(codename='delete_debate'))
        self.foo_mod.save()
        space.save()
        url = self.getURL(urln.DEBATE_DELETE,(), {'debate_id': self.foo_debate.id,
                                             'space_url': space.url})
        response = self.get(url)
        self.assertResponseOK(response)
        self.assertTemplateNotUsed(response, 'not_allowed.html')
        """
        When the mod doesn't have delete_debate permissions
        """
        self.foo_mod.user_permissions.remove(Permission.objects.get(codename='delete_debate'))
        self.foo_mod.save()
        space.save()
        response=self.get(url)
        self.assertResponseOK(response)
        self.assertTemplateUsed('not_allowed.html')
        self.logout()


        """
        Check if mods can delete from public space
        """


        space = self.bar_space
        self.login('bar_mod', 'bar_mod_password')
        self.assertTrue(self.isLoggedIn(self.bar_mod))
        self.bar_mod.user_permissions.add(Permission.objects.get(codename='delete_debate'))
        self.bar_mod.save()
        space.save()
        url = self.getURL(urln.DEBATE_DELETE,(), {'debate_id': self.bar_debate.id,
                                             'space_url': space.url})
        response = self.get(url)
        self.assertResponseOK(response)
        self.assertTemplateNotUsed(response, 'not_allowed.html')
        """
        When the mod doesn't have delete_debate permissions
        """
        self.bar_mod.user_permissions.remove(Permission.objects.get(codename='delete_debate'))
        self.bar_mod.save()
        space.save()
        response = self.get(url)
        self.assertResponseOK(response)
        self.assertTemplateUsed(response, 'not_allowed.html')
        self.logout()


        """
        Check if unregistered users cannot delete from public space
        """


        space = self.bar_space
        self.unreg_user = self.create_user('unreg_user', 'unreg_user_password')
        self.login('unreg_user','unreg_user_password')
        self.assertTrue(self.isLoggedIn(self.unreg_user))
        self.unreg_user.user_permissions.add(Permission.objects.get(codename='delete_debate'))
        self.unreg_user.save()
        space.save()
        url = self.getURL(urln.DEBATE_DELETE,(), {'debate_id': self.bar_debate.id,
                                             'space_url': space.url})
        response = self.get(url)
        self.assertResponseOK(response)
        self.assertTemplateUsed(response, 'not_allowed.html')
        """
        When the unreg-user doesn't have delete_debate permissions
        """
        self.unreg_user.user_permissions.remove(Permission.objects.get(codename='delete_debate'))
        self.unreg_user.save()
        space.save()
        response = self.get(url)
        self.assertResponseOK(response)
        self.assertTemplateUsed(response, 'not_allowed.html')
        self.logout()


        """
        Check if unregistered users cannot delete from private space
        """


        space = self.foo_space
        self.login('unreg_user', 'unreg_user_password')
        self.assertTrue(self.isLoggedIn(self.unreg_user))
        self.unreg_user.user_permissions.add(Permission.objects.get(codename='delete_debate'))
        self.unreg_user.save()
        space.save()
        url = self.getURL(urln.DEBATE_DELETE,(), {'debate_id': self.foo_debate.id,
                                             'space_url': space.url})
        response = self.get(url)
        self.assertResponseOK(response)
        self.assertTemplateUsed(response, 'not_allowed.html')
        """
        When the unreg_user doesn't have delete_debate permissions 
        """
        self.unreg_user.user_permissions.remove(Permission.objects.get(codename='delete_debate'))
        self.unreg_user.save()
        space.save()
        response = self.get(url)
        self.assertResponseOK(response)
        self.assertTemplateUsed(response, 'not_allowed.html')
        self.logout()
