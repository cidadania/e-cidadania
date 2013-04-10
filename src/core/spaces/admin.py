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
e-cidadania administration models for django-admin. This administration models
will make their respective data models available for management.
"""

from django.contrib import admin
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _

from core.spaces.models import Space, Entity, Document, Event, Intent


class EntityAdmin(admin.ModelAdmin):

    """
    Entities administration model.

    :list fields: name, website, space
    :search fields: name
    """
    list_display = ('name', 'website', 'space')
    search_fields = ('name',)


class EntityInline(admin.TabularInline):

    """
    TabularInline view for entities.
    """
    model = Entity


class SpaceAdmin(admin.ModelAdmin):

    """
    Administration view for django admin to create spaces. The save() method
    is overriden to store automatically the author of the space.

    :list fields: name, description, date
    :search fields: name
    """
    list_display = ('name', 'description', 'date')
    search_fields = ('name',)

    fieldsets = [
        (None, {'fields':
            [('name', 'url'), 'description']}),

        (_('Appearance'), {'fields':
            [('logo', 'banner')]}),

        (_('Modules'), {'fields':
            ('mod_cal', 'mod_docs', 'mod_news', 'mod_proposals',
            'mod_debate')}),
        (_('Staff'), {'fields':
            [('admins', 'mods', 'users')]}),
    ]

    inlines = [
        EntityInline,
    ]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.save()
        obj.users.add(request.user)

    def send_email(self, request, queryset):
        user_emails = queryset.objects.values('email')


class IntentAdmin(admin.ModelAdmin):

    """
    This is the administrative view to manage the request from users to
    participate on the spaces.
    """
    list_display = ('space', 'user', 'token', 'requested_on')
    search_fields = ('space', 'user')

    fieldsets = [
        (None, {'fields':
        ['user', 'space', 'token']})
    ]


class DocumentAdmin(admin.ModelAdmin):

    """
    Administration view to upload/modify documents. The save() method is
    overriden to store the author automatically.

    :list fields: title, space, docfile, author, pub_date
    :search fields: title, space, author, pub_date
    """
    list_display = ('title', 'space', 'docfile', 'author', 'pub_date')
    search_fields = ('title', 'space', 'author', 'pub_date')

    fieldsets = [
        (None, {'fields':
            ['title', 'docfile', 'space']}),
    ]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.save()


class EventAdmin(admin.ModelAdmin):

    """
    Meetings administration model.

    :list fields: title, space, meeting_date
    :search fields: title
    """
    list_display = ('title', 'space', 'event_date')
    search_fields = ('title',)

# This register line is commented because it collides with
# admin.autoregister() in the main urls.py file.

admin.site.register(Space, SpaceAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Entity, EntityAdmin)
admin.site.register(Intent, IntentAdmin)
