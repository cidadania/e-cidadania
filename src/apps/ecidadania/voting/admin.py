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

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from apps.ecidadania.voting.models import *


class ChoiceInline(admin.TabularInline):
        model = Choice


class PollAdmin(admin.ModelAdmin):
        list_display = ('question', 'pub_date', 'poll_lastup', 'author',
                                     'space')
        search_fields = ('question', 'author', 'space')

        inlines = [ChoiceInline]


class VotingAdmin(admin.ModelAdmin):

        list_display = ('title', 'start_date', 'end_date', 'author', 'space')
        search_fields = ('title', 'author', 'space')
admin.site.register(Poll, PollAdmin)
admin.site.register(Voting, VotingAdmin)
