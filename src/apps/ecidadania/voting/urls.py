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

from django.conf.urls import *
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

    url(r'^poll/(?P<pk>\d+)/$', ViewPoll.as_view(), name=VIEW_POLL),

    url(r'^poll/(?P<pk>\d+)/results/$', ViewPollResults.as_view(),
        name=VIEW_RESULT),

    url(r'^(?P<voting_id>\d+)/$', ViewVoting.as_view(), name=VIEW_VOTING),

    url(r'^vote/poll/(?P<poll_id>\d+)/$', 'polls.vote_poll', name=VOTE_POLL),

    url(r'^vote/voting/$', 'voting.vote_voting', name=VOTE_VOTING),

    url(r'^vote/validate/(?P<token>\w+)/$', 'voting.validate_voting',
        name=VALIDATE_VOTE),
)
