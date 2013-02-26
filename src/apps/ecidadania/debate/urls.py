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
from django.contrib.auth.decorators import permission_required
from apps.ecidadania.debate.views import ListDebates, ViewDebate, edit_debate 
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

    #(r'^edit/(?P<pk>\d+)', 'delete_debate'),

)
