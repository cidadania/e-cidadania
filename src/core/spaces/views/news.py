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

from django.views.generic.base import RedirectView
from django.views.generic.list import ListView
from django.views.generic.dates import ArchiveIndexView, MonthArchiveView, \
    YearArchiveView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from core.spaces import url_names as urln
from core.spaces.models import Space
from apps.ecidadania.news.models import Post
from core.permissions import has_space_permission, has_all_permissions


class RedirectArchive(RedirectView):

    """
    This class redirect any page to the news archive page (ListPosts)

    :rtype: Redirect (permanent)

    .. versionadded:: 0.1.6
    """
    permanent = True

    def get_redirect_url(self, **kwargs):
        space = self.kwargs['space_url']
        return reverse(urln.NEWS_ARCHIVE, kwargs={'space_url': space})


class YearlyPosts(YearArchiveView):

    """
    List all the news posts of the selected year. Uses default template naming.

    :rtype: Object list by date

    .. versionadded:: 0.1.6
    """
    make_object_list = True
    paginate_by = 12
    date_field = 'pub_date'

    def get_queryset(self):
        """
        We use the get queryset function to get only the posts relevant to
        a space, instead of all of them.
        """
        place = get_object_or_404(Space, url=self.kwargs['space_url'])
        return Post.objects.filter(space=place.id)

    def get_context_data(self, **kwargs):

        """
        Get extra context data for the ViewPost view.
        """
        context = super(YearlyPosts, self).get_context_data(**kwargs)
        context['get_place'] = get_object_or_404(Space,
            url=self.kwargs['space_url'])
        return context


class MonthlyPosts(MonthArchiveView):

    """
    List all the news posts for the selected month. This view uses default
    template naming.

    :rtype: Object list by date

    .. versionadded:: 0.1.6
    """
    paginate_by = 12
    date_field = 'pub_date'

    def get_queryset(self):
        """
        We use the get queryset function to get only the posts relevant to
        a space, instead of all of them.
        """
        place = get_object_or_404(Space, url=self.kwargs['space_url'])
        return Post.objects.filter(space=place.id)

    def get_context_data(self, **kwargs):

        """
        Get extra context data for the ViewPost view.
        """
        context = super(MonthlyPosts, self).get_context_data(**kwargs)
        context['get_place'] = get_object_or_404(Space,
            url=self.kwargs['space_url'])
        return context


class ListPosts(ArchiveIndexView):

    """
    List all post ordered by date
    """
    date_field = 'pub_date'
    paginate_by = 12
    allow_empty = True

    def get_queryset(self):
        """
        We use the get queryset function to get only the posts relevant to
        a space, instead of all of them.
        """
        place = get_object_or_404(Space, url=self.kwargs['space_url'])
        return Post.objects.filter(space=place.id)

    def get_context_data(self, **kwargs):

        """
        Get extra context data for the ViewPost view.
        """
        context = super(ListPosts, self).get_context_data(**kwargs)
        context['get_place'] = get_object_or_404(Space,
            url=self.kwargs['space_url'])
        return context
