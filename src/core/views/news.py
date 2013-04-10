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
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView

from apps.ecidadania.news.forms import NewsForm
from apps.ecidadania.news.models import Post


class ListNews(ListView):

    """
    List all the news within a space.
    """
    paginate_by = 10
    template_name = 'news/news_list.html'

    def get_queryset(self):
        news = Post.objects.all().filter(pub_index=True)

        return news


class AddPost(FormView):

    """
    This is a DRY violation. This is a reimplementation of the news view
    located at apps.news.views
    """
    form_class = NewsForm
    template_name = 'news/post_form.html'

    def get_success_url(self):
        return '/news/'

    def form_valid(self, form):
        form_uncommited = form.save(commit=False)
        form_uncommited.author = self.request.user
        form_uncommited.pub_index = True
        form_uncommited.save()
        messages.success(self.request, _('Post added successfully.'))
        return super(AddPost, self).form_valid(form)

    @method_decorator(permission_required('news.add_post'))
    def dispatch(self, *args, **kwargs):
        return super(AddPost, self).dispatch(*args, **kwargs)


class ViewPost(DetailView):

    """
    View a post with comments.
    """
    context_object_name = 'news'
    template_name = 'news/post_detail_index.html'

    def get_object(self):
        post_id = self.kwargs['post_id']
        return get_object_or_404(Post, pk=post_id)


class EditPost(UpdateView):

    """
    Edit an existent post.
    """
    model = Post
    template_name = 'news/post_form.html'
    success_url = '/'

    def get_object(self):
        cur_post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        return cur_post

    @method_decorator(permission_required('news.change_post'))
    def dispatch(self, *args, **kwargs):
        return super(EditPost, self).dispatch(*args, **kwargs)


class DeletePost(DeleteView):

    """
    Delete an existent post. Post deletion is only reserved to spaces
    administrators or site admins.
    """
    success_url = '/'

    def get_object(self):
        return get_object_or_404(Post, pk=self.kwargs['post_id'])

    @method_decorator(permission_required('news.delete_post'))
    def dispatch(self, *args, **kwargs):
        return super(DeletePost, self).dispatch(*args, **kwargs)
