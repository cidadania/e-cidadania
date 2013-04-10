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
from src.apps.ecidadania.proposals.models import Proposal, ProposalSet

from tests.test_utils import ECDTestCase


class ListProposalViewsTest(ECDTestCase):
    """
        Tests the views of proposals app.
    """
    
    def setUp(self):
        self.init()
        
    def testListProposalsView(self):
        """
            Tests ListProposal view.
        """
        user = self.create_user('test_user', 'abcde')
        other_user = self.create_user('other_test_user', 'acsrsd')
        space_properties = {'name': 'test_space', 'url': 'test_space_url',
                            'author': user, 'public': True}
        space1 = self.seed(Space, properties=space_properties)
        
        space_properties.update({'name': 'other_space', 'url': 'other_test_url',
                                'author': other_user, 'public': True})
        space2 = self.seed(Space, space_properties)
        
        proposal_properties = {'space': space1, 'author': user}
        proposal1 = self.seed(Proposal, properties=proposal_properties)
        proposal2 = self.seed(Proposal, properties=proposal_properties)
        proposals_list = [proposal1, proposal2]
        
        proposal_properties.update({'space': space2, 'author': other_user})
        proposal3 = self.seed(Proposal, properties=proposal_properties)
        proposal4 = self.seed(Proposal, properties=proposal_properties)
        proposal5 = self.seed(Proposal, properties=proposal_properties)
        other_proposals_list = [proposal3, proposal4, proposal5]
        url = self.getURL('list-proposals', kwargs={'space_url':space1.url})
        response = self.get(url)
        self.assertResponseOK(response)
        self.assertEqual(len(response.context[0].dicts[0]['proposal']), 
                         len(proposals_list))
        url = self.getURL('list-proposals', kwargs={'space_url': space2.url})
        response = self.get(url)
        self.assertResponseOK(response)
        self.assertEqual(len(response.context[0].dicts[0]['proposal']), 
                         len(other_proposals_list))
        
class ListProposalSetViewsTest(ECDTestCase):
    """
        Tests the views of proposalsets app.
    """
    
    def setUp(self):
        self.init()
        
    def testListProposalSetView(self):
        """
            Tests ListProposalSet view.
        """
        user = self.create_user('test_user', 'abcde')
        other_user = self.create_user('other_test_user', 'acsrsd')
        space_properties = {'name': 'test_space', 'url': 'test_space_url',
                            'author': user, 'public': True}
        space1 = self.seed(Space, properties=space_properties)
        
        space_properties.update({'name': 'other_space', 'url': 'other_test_url',
                                'author': other_user, 'public': True})
        space2 = self.seed(Space, space_properties)
        
        proposalset_properties = {'space': space1, 'author': user}
        proposalset1 = self.seed(ProposalSet, properties=proposalset_properties)
        proposalset2 = self.seed(ProposalSet, properties=proposalset_properties)
        proposalsets_list = [proposalset1, proposalset2]
        
        proposalset_properties.update({'space': space2, 'author': other_user})
        proposalset3 = self.seed(ProposalSet, properties=proposalset_properties)
        proposalset4 = self.seed(ProposalSet, properties=proposalset_properties)
        proposalset5 = self.seed(ProposalSet, properties=proposalset_properties)
        other_proposalsets_list = [proposalset3, proposalset4, proposalset5]
        url = self.getURL('list-proposalset', kwargs={'space_url':space1.url})
        response = self.get(url)
        self.assertResponseOK(response)
        self.assertEqual(len(response.context[0].dicts[0]['setlist']), 
                         len(proposalsets_list))
        url = self.getURL('list-proposalset', kwargs={'space_url': space2.url})
        response = self.get(url)
        self.assertResponseOK(response)
        self.assertEqual(len(response.context[0].dicts[0]['setlist']), 
                         len(other_proposalsets_list))
        
