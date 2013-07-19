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

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic.base import TemplateView, RedirectView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic import FormView
from django.template import RequestContext
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from guardian.shortcuts import assign_perm

from core.spaces import url_names as urln
from core.spaces.models import Space
from apps.ecidadania.news.models import Post
from apps.ecidadania.news.forms import NewsForm


class AddPost(FormView):

    """
    Create a new post. Only registered users belonging to a concrete group
    are allowed to create news. only site administrators will be able to
    post news in the index page.

    .. versionadded: 0.1

    :permissions required: admin_space, mod_space
    :parameters: space_url
    :context: get_place
    """
    form_class = NewsForm
    template_name = 'news/post_form.html'

    def dispatch(self, request, *args, **kwargs):
        space = get_object_or_404(Space, url=kwargs['space_url'])

        if (request.user.has_perm('admin_space', space) or
            request.user.has_perm('mod_space', space)):
            return super(AddPost, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_success_url(self):
        space = self.kwargs['space_url']
        return reverse(urln.SPACE_INDEX, kwargs={'space_url': space})

    def form_valid(self, form):
        self.space = get_object_or_404(Space, url=self.kwargs['space_url'])
        form_uncommited = form.save(commit=False)
        form_uncommited.author = self.request.user
        form_uncommited.space = self.space
        form_uncommited.save()
        return super(AddPost, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(AddPost, self).get_context_data(**kwargs)
        self.space = get_object_or_404(Space, url=self.kwargs['space_url'])
        context['get_place'] = self.space
        return context


class ViewPost(DetailView):

    """
    View a specific post.

    :permissions required: view_space
    """
    context_object_name = 'news'
    template_name = 'news/post_detail.html'

    def dispatch(self, request, *args, **kwargs):
        space = get_object_or_404(Space, url=kwargs['space_url'])

        if request.user.has_perm('view_space', space):
            return super(ViewPost, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_object(self):
        post = Post.objects.get(pk=self.kwargs['post_id'])
        try:
            post.views = post.views + 1
        except:
            post.views = 1
        post.save()
        return post

    def get_context_data(self, **kwargs):

        """
        Get extra context data for the ViewPost view.
        """
        context = super(ViewPost, self).get_context_data(**kwargs)
        context['get_place'] = get_object_or_404(Space, url=self.kwargs['space_url'])
        return context


class EditPost(UpdateView):

    """
    Edit an existent post.

    :permissions required: admin_space, mod_space
    :parameters: space_url, post_id
    :context: get_place
    """
    model = Post
    template_name = 'news/post_form.html'

    def dispatch(self, request, *args, **kwargs):
        space = get_object_or_404(Space, url=kwargs['space_url'])

        if (request.user.has_perm('admin_space', space) or
            request.user.has_perm('mod_space', space)):
            return super(EditPost, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def form_valid(self, form):
        self.space = get_object_or_404(Space, url=self.kwargs['space_url'])
        form_uncommited = form.save(commit=False)
        form_uncommited.author = self.request.user
        form_uncommited.space = self.space
        form_uncommited.save()
        return super(EditPost, self).form_valid(form)

    def get_success_url(self):
        space = self.kwargs['space_url']
        return reverse(urln.SPACE_INDEX, kwargs={'space_url': space})

    def get_object(self):
        cur_post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        return cur_post

    def get_context_data(self, **kwargs):
        context = super(EditPost, self).get_context_data(**kwargs)
        context['get_place'] = get_object_or_404(Space, url=self.kwargs['space_url'])
        return context


class DeletePost(DeleteView):

    """
    Delete an existent post. Post deletion is only reserved to spaces
    administrators or site admins.
    """
    context_object_name = "get_place"

    def dispatch(self, request, *args, **kwargs):
        space = get_object_or_404(Space, url=kwargs['space_url'])

        if (request.user.has_perm('admin_space', space) or
            request.user.has_perm('mod_space', space)):
            return super(DeletePost, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_success_url(self):
        space = self.kwargs['space_url']
        return reverse(urln.SPACE_INDEX, kwargs={'space_url': space})

    def get_object(self):
        return get_object_or_404(Post, pk=self.kwargs['post_id'])

    def get_context_data(self, **kwargs):

        """
        Get extra context data for the ViewPost view.
        """
        context = super(DeletePost, self).get_context_data(**kwargs)
        context['get_place'] = get_object_or_404(Space, url=self.kwargs['space_url'])
        return context
