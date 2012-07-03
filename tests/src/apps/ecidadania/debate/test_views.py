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

from tests.test_utils import ECDTestCase


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
        url = self.getURL('list-debates', kwargs={'space_url':space1.url})
        response = self.get(url)
        #print self.printResponse(response)
        self.assertResponseOK(response)
        self.assertEqual(len(response.context[0].dicts[0]['debate_list']), 
                         len(debates_list))
        
        url = self.getURL('list-debates', kwargs={'space_url': space2.url})
        response = self.get(url)
        self.assertResponseOK(response)
        self.assertEqual(len(response.context[0].dicts[0]['debate_list']), 
                         len(other_debates_list))
        
    def testViewDebate(self):
        """Tests ViewDebate view.
        """
        url = self.getURL('view-debate',(), {'debate_id': self.user_debate.id,
                                             'space_url': self.user_space.url})
        response = self.get(url)
        self.assertResponseOK(response)
        context = response.context[0].dicts[0]
        assert 'notes' in context
        assert 'columns' in context
        assert 'rows' in context
        assert 'get_place' in context
        print context['columns']
        self.assertEqual(len(context['notes']), 1)
        self.assertEqual(len(context['columns']), 1)
        self.assertEqual(len(context['rows']), 1)
        
        url = self.getURL('view-debate',(), {'debate_id': 5,
                                             'space_url': self.user_space.url})
        response = self.get(url)
        self.assertResponseNotFound(response)