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
The proposal administration allows to edit every proposal made in the system.
"""

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from apps.ecidadania.proposals.models import Proposal, ProposalSet, ProposalField


class ProposalSetAdmin(admin.ModelAdmin):

    """
    Basic ProposalSet administration interface.

    :list_display: name, author
    :search: none
    """

    list_display = ('name', 'author')

    fieldsets = [
        (None, {'fields': ['name']})
    ]


class ProposalAdmin(admin.ModelAdmin):

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


class ProposalFieldAdmin(admin.ModelAdmin):

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
