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

from core.spaces.views.spaces import ViewSpaceIndex, ListSpaces, \
    DeleteSpace, EditRole
from core.spaces.views.documents import ListDocs, DeleteDocument, \
    AddDocument, EditDocument
from core.spaces.views.events import ListEvents, DeleteEvent, ViewEvent, \
    AddEvent, EditEvent
from core.spaces.views.rss import SpaceFeed
from core.spaces.views.intent import ValidateIntent
from core.spaces.views.news import ListPosts, YearlyPosts, MonthlyPosts, \
    RedirectArchive
from core.spaces.url_names import *

# NOTICE: Don't change the order of urlpatterns or it will probably break.

urlpatterns = patterns('',

    # RSS Feed
    url(r'^(?P<space_url>\w+)/rss/$', SpaceFeed(), name=SPACE_FEED),

    # News
    url(r'^(?P<space_url>\w+)/news/',
        include('apps.ecidadania.news.urls')),

    # Proposals
    url(r'^(?P<space_url>\w+)/proposal/',
        include('apps.ecidadania.proposals.urls')),

    # Calendar
    url(r'^(?P<space_url>\w+)/calendar/',
        include('apps.ecidadania.cal.urls')),

    # Debates
    url(r'^(?P<space_url>\w+)/debate/',
        include('apps.ecidadania.debate.urls')),

    # Votes
    url(r'^(?P<space_url>\w+)/voting/',
        include('apps.ecidadania.voting.urls')),

)

# Document URLs
urlpatterns += patterns('',

    url(r'^(?P<space_url>\w+)/docs/add/$', AddDocument.as_view(),
        name=DOCUMENT_ADD),

    url(r'^(?P<space_url>\w+)/docs/(?P<doc_id>\d+)/edit/$',
        EditDocument.as_view(), name=DOCUMENT_EDIT),

    url(r'^(?P<space_url>\w+)/docs/(?P<doc_id>\d+)/delete/$',
        DeleteDocument.as_view(), name=DOCUMENT_DELETE),

    url(r'^(?P<space_url>\w+)/docs/$', ListDocs.as_view(),
        name=DOCUMENT_LIST),

)

# Event URLs
urlpatterns += patterns('',

    url(r'^(?P<space_url>\w+)/event/add/$', AddEvent.as_view(),
        name=EVENT_ADD),

    url(r'^(?P<space_url>\w+)/event/(?P<event_id>\d+)/edit/$',
        EditEvent.as_view(), name=EVENT_EDIT),

    url(r'^(?P<space_url>\w+)/event/(?P<event_id>\d+)/delete/$',
        DeleteEvent.as_view(), name=EVENT_DELETE),

    url(r'^(?P<space_url>\w+)/event/(?P<event_id>\d+)/$',
        ViewEvent.as_view(), name=EVENT_VIEW),

    url(r'^(?P<space_url>\w+)/event/$', ListEvents.as_view(),
        name=EVENT_LIST),

)

# Intent URLs
urlpatterns += patterns('',

    url(r'^(?P<space_url>\w+)/intent/$',
        'core.spaces.views.intent.add_intent', name=INTENT_ADD),

    url(r'^(?P<space_url>\w+)/intent/approve/(?P<token>\w+)/$',
        ValidateIntent.as_view(), name=INTENT_VALIDATE),

)

# Spaces URLs
urlpatterns += patterns('',

    url(r'^(?P<space_url>\w+)/edit/',
        'core.spaces.views.spaces.edit_space', name=SPACE_EDIT),

    url(r'^(?P<space_url>\w+)/delete/', DeleteSpace.as_view(),
        name=SPACE_DELETE),

    url(r'^(?P<space_url>\w+)/news/$', RedirectArchive.as_view(),
        name=SPACE_NEWS),

    url(r'^(?P<space_url>\w+)/news/archive/$', ListPosts.as_view(),
        name=NEWS_ARCHIVE),

    url(r'^(?P<space_url>\w+)/news/archive/(?P<year>\d{4})/$',
        YearlyPosts.as_view(), name=NEWS_YEAR),

    url(r'^(?P<space_url>\w+)/news/archive/(?P<year>\d{4})/(?P<month>\w+)/$',
        MonthlyPosts.as_view(), name=NEWS_MONTH),

    url(r'^add/$', 'core.spaces.views.spaces.create_space',
        name=SPACE_ADD),

    url(r'^$', ListSpaces.as_view(), name=SPACE_LIST),

    # url(_(r'^go/'), GoToSpace.as_view(), name=GOTO_SPACE),

    url(r'^(?P<space_url>\w+)/roles/', EditRole.as_view(),
        name=EDIT_ROLES),

    url(r'^(?P<space_url>\w+)/$', ViewSpaceIndex.as_view(),
        name=SPACE_INDEX),

)
