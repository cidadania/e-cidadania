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
from django.utils.translation import ugettext_lazy as _

from guardian.admin import GuardedModelAdmin

from apps.ecidadania.staticpages.models import StaticPage


class PageAdmin(GuardedModelAdmin):

    """
    """
    list_display = ('name', 'uri', 'pub_date', 'author')
    search_fields = ('name', 'uri', 'author')

    # change_form_template = 'staticpages/change_form.html'

    fieldsets = [
        (None, {'fields':
            [('name', 'uri')]}),

        (_('Description'), {'fields':
            [('content')]}),

        (_('Options'), {'fields':
            [('show_footer', 'order')]})
    ]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.save()

admin.site.register(StaticPage, PageAdmin)
