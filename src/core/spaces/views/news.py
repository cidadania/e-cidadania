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

from django.views.generic.base import RedirectView
from django.views.generic.list import ListView
from django.views.generic.dates import ArchiveIndexView, MonthArchiveView, \
    YearArchiveView
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied

from core.spaces import url_names as urln
from core.spaces.models import Space
from apps.ecidadania.news.models import Post


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

    def dispatch(self, request, *args, **kwargs):
        space = get_object_or_404(Space, url=kwargs['space_url'])

        if request.user.has_perm('view_space', space):
            return super(YearlyPosts, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

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

    def dispatch(self, request, *args, **kwargs):
        space = get_object_or_404(Space, url=kwargs['space_url'])

        if request.user.has_perm('view_space', space):
            return super(MonthlyPosts, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

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

    def dispatch(self, request, *args, **kwargs):
        space = get_object_or_404(Space, url=kwargs['space_url'])

        if request.user.has_perm('view_space', space):
            return super(ListPosts, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

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
