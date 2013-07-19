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
e-cidadania administration models for django-admin. This administration models
will make their respective data models available for management.
"""

from django.contrib import admin
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _

from guardian.admin import GuardedModelAdmin

from core.spaces.models import Space, Entity, Document, Event, Intent


class EntityAdmin(GuardedModelAdmin):

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


class SpaceAdmin(GuardedModelAdmin):

    """
    Administration view for django admin to create spaces. The save() method
    is overriden to store automatically the author of the space.

    :list fields: name, description, date
    :search fields: name
    """
    list_display = ('name', 'description', 'pub_date')
    search_fields = ('name',)

    fieldsets = [
        (None, {'fields':
            [('name', 'url'), 'description']}),

        (_('Appearance'), {'fields':
            [('logo', 'banner')]}),

        (_('Modules'), {'fields':
            ('mod_cal', 'mod_docs', 'mod_news', 'mod_proposals',
            'mod_debate')}),
    ]

    inlines = [
        EntityInline,
    ]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.save()

    def send_email(self, request, queryset):
        user_emails = queryset.objects.values('email')


class IntentAdmin(GuardedModelAdmin):

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


class DocumentAdmin(GuardedModelAdmin):

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


class EventAdmin(GuardedModelAdmin):

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
