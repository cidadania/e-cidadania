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

import itertools
import base64

from django.contrib.syndication.views import Feed
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate, login
from django.http import HttpResponse

from apps.ecidadania.proposals.models import Proposal
from apps.ecidadania.debate.models import Debate
from apps.ecidadania.news.models import Post
from core.spaces.models import Space, Event


class HTTPAuthFeed(Feed):
    basic_auth_realm = 'e-cidadania'

    def __call__(self, request, *args, **kwargs):
        # HTTP auth check inspired by http://djangosnippets.org/snippets/243/
        if request.user.is_authenticated():
            # already logged in
            return super(HTTPAuthFeed, self).__call__(request, *args, **kwargs)

        # check HTTP auth credentials
        if 'HTTP_AUTHORIZATION' in request.META:
            auth = request.META['HTTP_AUTHORIZATION'].split()
            if len(auth) == 2:
                # only basic auth is supported
                if auth[0].lower() == "basic":
                    uname, passwd = base64.b64decode(auth[1]).split(':')
                    user = authenticate(username=uname, password=passwd)
                    if user is not None:
                        if user.is_active:
                            login(request, user)
                            request.user = user
                            return super(HTTPAuthFeed, self).__call__(request,
                                *args, **kwargs)

        # missing auth header or failed authentication results in 401
        response = HttpResponse()
        response.status_code = 401
        response['WWW-Authenticate'] = 'Basic realm="%s"' % self.basic_auth_realm
        return response


class SpaceFeed(HTTPAuthFeed):

    """
    Returns a space feed with the content of various applications. In the
    future this function must detect applications and returns their own feeds.
    """

    def get_object(self, request, space_url):
        current_space = get_object_or_404(Space, url=space_url)
        return current_space

    def title(self, obj):
        return _("%s") % obj.name

    def link(self, obj):
        return obj.get_absolute_url()

    def description(self, obj):
        return _("All the recent activity in %s ") % obj.name

    def items(self, obj):
        results = itertools.chain(
            Post.objects.filter(space=obj).order_by('-pub_date')[:10],
            Proposal.objects.filter(space=obj).order_by('-pub_date')[:10],
            Event.objects.filter(space=obj).order_by('-pub_date')[:10],
            Debate.objects.filter(space=obj).order_by('-date')[:10]
        )
        return results

    def item_title(self, item):
        return type(item).__name__ + ": " + item.title

    def item_description(self, item):
        return item.description

        return sorted(results, key=lambda x: x.pub_date, reverse=True)
