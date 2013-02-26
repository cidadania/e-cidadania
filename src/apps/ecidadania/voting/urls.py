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

from django.conf.urls import *
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from apps.ecidadania.voting.views.polls import ViewPoll, DeletePoll, \
    ListPolls, ViewPollResults
from apps.ecidadania.voting.views.voting import ViewVoting, ListVotings, \
    AddVoting, EditVoting, DeleteVoting
from apps.ecidadania.voting.url_names import *


urlpatterns = patterns('apps.ecidadania.voting.views',

    url(r'^$', ListVotings.as_view(), name=LIST_VOTING),

    url(r'^poll/$', ListPolls.as_view(), name=LIST_POLL),

    url(r'^add/$', AddVoting.as_view(), name=ADD_VOTING),

    url(r'^add/poll/$', 'polls.add_poll', name=ADD_POLL),

    url(r'^poll/(?P<poll_id>\d+)/edit/$', 'polls.edit_poll', name=EDIT_POLL),

    url(r'^(?P<voting_id>\d+)/edit/$', EditVoting.as_view(),
        name=EDIT_VOTING),
        
    url(r'^poll/(?P<poll_id>\d+)/delete/$', DeletePoll.as_view(),
        name=DELETE_POLL),
        
    url(r'^(?P<voting_id>\d+)/delete/$', DeleteVoting.as_view(),
        name=DELETE_VOTING),
        
    url(_(r'^poll/(?P<pk>\d+)/$'), ViewPoll.as_view(), name=VIEW_POLL),

    url(_(r'^poll/(?P<pk>\d+)/results/$'), ViewPollResults.as_view(),
        name=VIEW_RESULT),

    url(r'^(?P<voting_id>\d+)/$', ViewVoting.as_view(), name=VIEW_VOTING),

    url(r'^vote/poll/(?P<poll_id>\d+)/$', 'polls.vote_poll', name=VOTE_POLL),

    url(r'^vote/voting/$', 'voting.vote_voting', name=VOTE_VOTING),

    url(r'^vote/validate/(?P<token>\w+)/$', 'voting.validate_voting',
        name=VALIDATE_VOTE),
)




