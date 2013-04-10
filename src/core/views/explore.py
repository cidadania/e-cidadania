#/usr/bin/env python
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

from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response
from django.template import RequestContext

from core.spaces.models import Space
from apps.ecidadania.news.models import Post


def explore(request):

    """
    This view provides a list of all the recent activity happening in the
    platform like new spaces, latest news on public spaces, etc.

    .. versionadded:: 0.1.8
    """
    spaces = Space.objects.all()
    recent_spaces = Space.objects.all().order_by('-date')[:5]
    news = Post.objects.filter(space__public=True).order_by('-pub_date')

    extra_context = {
        'recent_spaces': recent_spaces,
        'spaces': spaces,
        'news': news,
    }

    return render_to_response('explore.html', extra_context,
        context_instance=RequestContext(request))
