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
The proposal administration allows to edit every proposal made in the system.
"""

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from guardian.admin import GuardedModelAdmin

from apps.ecidadania.proposals.models import Proposal, ProposalSet, ProposalField


class ProposalSetAdmin(GuardedModelAdmin):

    """
    Basic ProposalSet administration interface.

    :list_display: name, author
    :search: none
    """

    list_display = ('name', 'author')

    fieldsets = [
        (None, {'fields': ['name']})
    ]


class ProposalAdmin(GuardedModelAdmin):

    """
    Basic proposal administration interface since most of the work is done
    in the website.

    :list display: title, author, tags
    :search: none:
    """
    list_display = ('title', 'author', 'tags')

    fieldsets = [
        (None, {'fields':
            ['code', 'title', 'proposalset', 'description', 'tags',
            'support_votes']}),

        (_('Location'), {'fields':
            ['latitude', 'longitude']}),

        (_('Relations'), {'fields':
            [('space', 'author')]}),

        (_('Other'), {'fields':
            ['budget', 'closed', 'close_reason', 'closed_by']}),

        (_('Options'), {'fields':
            ['anon_allowed', 'refurbished']}),

    ]


class ProposalFieldAdmin(GuardedModelAdmin):

    """
    Basic proposal administration interface since most part is done in
    the website.

    :list display: proposalset, field_name
    :search:none

    .. versionadded:: 0.1.5b
    """
    list_display = ('proposalset', 'field_name')

    fieldsets = [
        (None, {'fields':
            ['proposalset', 'field_name']}),
    ]


admin.site.register(ProposalSet, ProposalSetAdmin)
admin.site.register(Proposal, ProposalAdmin)
admin.site.register(ProposalField, ProposalFieldAdmin)
