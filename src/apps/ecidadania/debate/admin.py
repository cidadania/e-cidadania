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

from django.contrib import admin

from guardian.admin import GuardedModelAdmin

from apps.ecidadania.debate.models import Debate, Note, Column, Row


class ColumnInline(admin.TabularInline):

    """
    This TabularInline form allows the user to add the debate Columns in the same
    form as the debate.
    """
    model = Column
    extra = 2


class RowInline(admin.TabularInline):

    """
    This TabularInline form allows the user to add the debate Rows in the same
    form as the debate.
    """
    model = Row
    extra = 2


class DebateAdmin(GuardedModelAdmin):

    """
    Administration for all the debates.
    """
    list_display = ('title', 'date')
    inlines = [ColumnInline, RowInline]


class NoteAdmin(GuardedModelAdmin):

    """
    Administration for all the notes in every debate.
    """
    list_display = ('message', 'date', 'author')

admin.site.register(Debate, DebateAdmin)
admin.site.register(Note, NoteAdmin)
