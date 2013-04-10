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

from apps.ecidadania.staticpages.models import StaticPage


class PageAdmin(admin.ModelAdmin):

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
