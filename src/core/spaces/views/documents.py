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

from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic import FormView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from core.spaces import url_names as urln
from core.spaces.models import Space, Document
from core.spaces.forms import SpaceForm, DocForm
from core.permissions import has_space_permission, has_all_permissions


class AddDocument(FormView):

    """
    Upload a new document and attach it to the current space.

    :rtype: Object
    :context: form, get_place
    """
    form_class = DocForm
    template_name = 'spaces/document_form.html'

    def get_success_url(self):
        space = self.kwargs['space_url']
        return reverse(urln.SPACE_INDEX, kwargs={'space_url': space})

    def form_valid(self, form):
        self.space = get_object_or_404(Space, url=self.kwargs['space_url'])
        form_uncommited = form.save(commit=False)
        form_uncommited.space = self.space
        form_uncommited.author = self.request.user
        form_uncommited.save()
        # print form.cleaned_data
        return super(AddDocument, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(AddDocument, self).get_context_data(**kwargs)
        space = get_object_or_404(Space, url=self.kwargs['space_url'])
        context['get_place'] = space
        context['user_is_admin'] = (has_space_permission(self.request.user,
            space, allow=['admins', 'mods']) or has_all_permissions(
                self.request.user))
        return context

    @method_decorator(permission_required('spaces.add_document'))
    def dispatch(self, *args, **kwargs):
        return super(AddDocument, self).dispatch(*args, **kwargs)


class EditDocument(UpdateView):

    """
    Returns a DocForm filled with the current document data.

    :rtype: HTML Form
    :context: doc, get_place
    """
    model = Document
    template_name = 'spaces/document_form.html'

    def get_success_url(self):
        space = self.kwargs['space_url']
        return reverse(urln.SPACE_INDEX, kwargs={'space_url': space})

    def get_object(self):
        cur_doc = get_object_or_404(Document, pk=self.kwargs['doc_id'])
        return cur_doc

    def get_context_data(self, **kwargs):
        context = super(EditDocument, self).get_context_data(**kwargs)
        space = get_object_or_404(Space, url=self.kwargs['space_url'])
        context['get_place'] = space
        context['user_is_admin'] = (has_space_permission(self.request.user,
            space, allow=['admins', 'mods']) or has_all_permissions(
                self.request.user))
        return context

    @method_decorator(permission_required('spaces.change_document'))
    def dispatch(self, *args, **kwargs):
        return super(EditDocument, self).dispatch(*args, **kwargs)


class DeleteDocument(DeleteView):

    """
    Returns a confirmation page before deleting the current document.

    :rtype: Confirmation
    :context: get_place
    """

    def get_object(self):
        return get_object_or_404(Document, pk=self.kwargs['doc_id'])

    def get_success_url(self):
        space = self.kwargs['space_url']
        return reverse(urln.SPACE_INDEX, kwargs={'space_url': space})

    def get_context_data(self, **kwargs):
        context = super(DeleteDocument, self).get_context_data(**kwargs)
        context['get_place'] = get_object_or_404(Space,
            url=self.kwargs['space_url'])
        return context

    @method_decorator(permission_required('spaces.delete_document'))
    def dispatch(self, *args, **kwargs):
        return super(DeleteDocument, self).dispatch(*args, **kwargs)


class ListDocs(ListView):

    """
    Returns a list of documents attached to the current space.

    :rtype: Object list
    :context: object_list, get_place
    """
    paginate_by = 25
    context_object_name = 'document_list'

    def get_queryset(self):
        place = get_object_or_404(Space, url=self.kwargs['space_url'])
        objects = Document.objects.all().filter(space=place.id) \
            .order_by('pub_date')

        cur_user = self.request.user
        if has_space_permission(cur_user, place,
                                allow=['admins', 'mods', 'users']):
            return objects

        if self.request.user.is_anonymous():
            self.template_name = 'not_allowed.html'
            return objects

        self.template_name = 'not_allowed.html'
        return objects

    def get_context_data(self, **kwargs):
        context = super(ListDocs, self).get_context_data(**kwargs)
        context['get_place'] = get_object_or_404(Space,
            url=self.kwargs['space_url'])
        return context
