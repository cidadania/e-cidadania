# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Clione Software
# Copyright (c) 2010-2013 Cidadania S. Coop. Galega
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Proposal module URLs.
"""

from django.conf.urls import patterns, url

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
