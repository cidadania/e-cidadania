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
This file contains all the URLs that e_cidadania will inherit when the user
access to '/spaces/'.
"""
from django.conf.urls import *
from django.utils.translation import ugettext_lazy as _

from core.spaces.views import GoToSpace, ViewSpaceIndex, ListSpaces,\
                                          DeleteSpace, ListDocs, DeleteDocument, \
                                          ListEvents, DeleteEvent, ViewEvent, \
                                          ListPosts, SpaceFeed, AddDocument, \
                                          EditDocument, AddEvent, EditEvent, \
                                          ValidateIntent, EditRole

# NOTICE: Don't change the order of urlpatterns or it will probably break.

urlpatterns = patterns('core.spaces.views',

    # RSS Feed
    url(_(r'^(?P<space_url>\w+)/rss/$'), SpaceFeed(), name='space-feed'),
    
    # News
    url(_(r'^(?P<space_url>\w+)/news/'), include('apps.ecidadania.news.urls')),

    # Proposals
    url(_(r'^(?P<space_url>\w+)/proposal/'), include('apps.ecidadania.proposals.urls')),
    
    # Calendar
    url(_(r'^(?P<space_url>\w+)/calendar/'), include('apps.ecidadania.cal.urls')),

    # Debates
    url(_(r'^(?P<space_url>\w+)/debate/'), include('apps.ecidadania.debate.urls')),
    
    # Debates
    url(_(r'^(?P<space_url>\w+)/voting/'), include('apps.ecidadania.voting.urls')),

)

# Document URLs
urlpatterns += patterns('core.spaces.views',

    url(_(r'^(?P<space_url>\w+)/docs/add/$'), AddDocument.as_view(), name='add-document'),

    url(_(r'^(?P<space_url>\w+)/docs/(?P<doc_id>\d+)/edit/$'), EditDocument.as_view(), name='edit-document'),

    url(_(r'^(?P<space_url>\w+)/docs/(?P<doc_id>\d+)/delete/$'), DeleteDocument.as_view(), name='delete-document'),

    url(_(r'^(?P<space_url>\w+)/docs/$'), ListDocs.as_view(), name='list-documents'),

)

# Event URLs
urlpatterns += patterns('core.spaces.views',

    url(_(r'^(?P<space_url>\w+)/event/add/$'), AddEvent.as_view(), name='add-event'),

    url(_(r'^(?P<space_url>\w+)/event/(?P<event_id>\d+)/edit/$'), EditEvent.as_view(), name='edit-event'),

    url(_(r'^(?P<space_url>\w+)/event/(?P<event_id>\d+)/delete/$'), DeleteEvent.as_view(), name='delete-event'),

    url(_(r'^(?P<space_url>\w+)/event/(?P<event_id>\d+)/$'), ViewEvent.as_view(), name='view-event'),

    url(_(r'^(?P<space_url>\w+)/event/$'), ListEvents.as_view(), name='list-events'),

)

# Intent URLs
urlpatterns += patterns('core.spaces.views',

    url(_(r'^(?P<space_url>\w+)/intent/$'), 'add_intent', name='add-intent'),
    url(_(r'^(?P<space_url>\w+)/intent/approve/(?P<token>\w+)/$'), ValidateIntent.as_view(), name='validate-intent'),

)

# Spaces URLs
urlpatterns += patterns('core.spaces.views',

    url(_(r'^(?P<space_url>\w+)/edit/'), 'edit_space', name='edit-space'),

    url(_(r'^(?P<space_url>\w+)/delete/'), DeleteSpace.as_view(), name='delete-space'),
    
    url(_(r'^(?P<space_url>\w+)/news/'), ListPosts.as_view(), name='list-space-news'),
        
    url(_(r'^add/$'), 'create_space', name='create-space'),

    url(r'^$', ListSpaces.as_view(), name='list-spaces'),

    url(_(r'^go/'), GoToSpace.as_view(), name='goto-space'),

    url(_(r'^(?P<space_url>\w+)/roles/'), EditRole.as_view(), name='edit-roles'),

    url(r'^(?P<space_url>\w+)/$', ViewSpaceIndex.as_view(), name='space-index'),

)


