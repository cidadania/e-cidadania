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

"""
Proposal module URLs.
"""

from django.conf.urls import *

from apps.ecidadania.proposals.views.common import ViewProposal, \
    support_proposal
from apps.ecidadania.proposals.views.proposals import AddProposal, \
    EditProposal, DeleteProposal, ListProposals
from apps.ecidadania.proposals.views.proposalsets import AddProposalSet, \
    EditProposalSet, DeleteProposalSet, add_proposal_field, \
    delete_proposal_field, proposal_to_set, mergedproposal_to_set, \
    ListProposalSet, ViewProposalSet, AddProposalInSet
from apps.ecidadania.proposals.url_names import *


urlpatterns = patterns('apps.ecidadania.proposals.views',

    url(r'^set/$', ListProposalSet.as_view(), name=PROPOSALSET_LIST),

    url(r'^set/(?P<set_id>\w+)/$', ViewProposalSet.as_view(),
        name=PROPOSALSET_VIEW),

    url(r'^set/(?P<set_id>\w+)/add/$', AddProposalInSet.as_view(),
        name=PROPOSAL_ADD_INSET),

    url(r'^add/$', AddProposal.as_view(), name=PROPOSAL_ADD),

    url(r'^add/set/$', AddProposalSet.as_view(), name=PROPOSALSET_ADD),

    url(r'^add/field/', 'proposalsets.add_proposal_field',
        name=PROPOSALFIELD_ADD),

    url(r'^edit/(?P<prop_id>\w+)/', EditProposal.as_view(),
        name=PROPOSAL_EDIT),

    url(r'^edit/set/(?P<p_set>\w+)/', EditProposalSet.as_view(),
        name=PROPOSALSET_EDIT),

    url(r'^delete/field/$', 'proposalsets.delete_proposal_field',
        name=PROPOSALFIELD_DELETE),

    url(r'^delete/(?P<prop_id>\w+)/$', DeleteProposal.as_view(),
        name=PROPOSAL_DELETE),

    url(r'^delete/set/(?P<p_set>\w+)/$', DeleteProposalSet.as_view(),
        name=PROPOSALSET_DELETE),

    url(r'^support/', 'common.support_proposal', name=PROPOSAL_VOTE),

    url(r'^merge/(?P<set_id>\w+)/', 'proposals.merge_proposal',
        name=PROPOSAL_MERGED),

    url(r'^merge_proposals/', 'proposalsets.mergedproposal_to_set',
        name=PROPOSAL_MERGEDTOSET),

    url(r'^select_set/', 'proposalsets.proposal_to_set', name=SELECT_SET),

    url(r'^(?P<prop_id>\w+)/$', ViewProposal.as_view(), name=PROPOSAL_VIEW),

    url(r'^$', ListProposals.as_view(), name=PROPOSAL_LIST),

    # url(_(r'^(?P<space_url>\w+)/vote/approve/(?P<token>\w+)/$'),
    #    ValidateVote.as_view(), name=VALIDATE_VOTE),
)
