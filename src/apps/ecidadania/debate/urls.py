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
This file contains all the URLs that e_cidadania will inherit when the user
access to '/spaces/'.
"""
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import permission_required
from apps.ecidadania.debate.views import ListDebates, ViewDebate, DeleteDebate, edit_debate
from apps.ecidadania.debate.url_names import *

urlpatterns = patterns('apps.ecidadania.debate.views',

    url(r'^$', ListDebates.as_view(), name=DEBATE_LIST),

    url(r'^(?P<debate_id>\d+)/', ViewDebate.as_view(), name=DEBATE_VIEW),

    url(r'^add/', 'add_new_debate', name=DEBATE_ADD),

    url(r'^update_position/', 'update_position', name=NOTE_UPDATE_POSITION),

    url(r'^update_note/', 'update_note', name=NOTE_UPDATE),

    url(r'^create_note/', 'create_note', name=NOTE_ADD),

    url(r'^delete_note/', 'delete_note', name=NOTE_DELETE),

    # Editing debates is not allowed at this time
    url(r'^edit/(?P<debate_id>\d+)/', 'edit_debate', name=DEBATE_EDIT),

    url(r'^delete/(?P<debate_id>\d+)', DeleteDebate.as_view(), name=DEBATE_DELETE),

)
