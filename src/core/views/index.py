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


from django.contrib import messages
from django.contrib.syndication.views import Feed
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from apps.ecidadania.news.forms import NewsForm
from apps.ecidadania.news.models import Post
from apps.ecidadania.staticpages.models import StaticPage

from core.spaces.models import Space

from e_cidadania import settings


def index_view(request):

    """
    Main view for the index page. It's separated from the urls.py file
    because using direct_to_template in urls.py doesn't refresh the content
    (it's loaded only once).
    """
    pub = Post.objects.filter(pub_index=True).order_by('-pub_date')
    space_list = Space.objects.all()
    recent_spaces = Space.objects.all().order_by('-date')[:5]
    page_list = StaticPage.objects.filter(show_footer=True).order_by('-order')

    extra_context = {
        'publication': pub,
        'spaces': space_list,
        'recent_spaces': recent_spaces,
        'page': page_list,
        'version': settings.__version__,
        'status': settings.__status__,
        'debug_mode': settings.DEBUG,
        #'cache_timeout': 500,
    }

    if request.user.is_anonymous():
        messages.info(request, _("Hi! It seems that it's your first time \
        here. Maybe you want to <a href=\"/accounts/register\">register</a> \
        or <a href=\"/accounts/login/\">login</a> if you have an account."))
    return render_to_response('site_index.html', extra_context,
                              context_instance=RequestContext(request))


class IndexEntriesFeed(Feed):

    """
    Creates an RSS feed out of the news posts in the index page.

    :rtype: RSS Feed
    :context: None

    .. versionadded:: 0.1b
    """
    title = _('e-cidadania news')
    link = '/news/'
    description = _('Updates on the main e-cidadania site.')

    def items(self):
        """
        Get all the posts published publicly.
        """
        return Post.objects.all().order_by('-pub_date')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description
