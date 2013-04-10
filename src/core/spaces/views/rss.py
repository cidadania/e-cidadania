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
