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
    spaces = Space.objects.all().filter(public=True)
    recent_spaces = Space.objects.all().order_by('-date')[:5]
    news = Post.objects.filter(space__public=True).order_by('-pub_date')

    extra_context = {
        'recent_spaces': recent_spaces,
        'spaces': spaces,
        'news': news,
    }

    return render_to_response('explore.html', extra_context,
        context_instance=RequestContext(request))
