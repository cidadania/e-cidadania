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

from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic import FormView
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied

from core.spaces import url_names as urln
from core.spaces.models import Space, Document
from core.spaces.forms import SpaceForm, DocForm


class AddDocument(FormView):

    """
    Upload a new document and attach it to the current space.

    :permissions required: admin_space, mod_space
    :rtype: Object
    :context: form, get_place
    """
    form_class = DocForm
    template_name = 'spaces/document_form.html'

    def dispatch(self, request, *args, **kwargs):
        space = get_object_or_404(Space, url=kwargs['space_url'])

        if (request.user.has_perm('admin_space', space) or
            request.user.has_perm('mod_space', space)):
            return super(AddDocument, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_success_url(self):
        space = self.kwargs['space_url']
        return reverse(urln.SPACE_INDEX, kwargs={'space_url': space})

    def form_valid(self, form):
        self.space = get_object_or_404(Space, url=self.kwargs['space_url'])
        form_uncommited = form.save(commit=False)
        form_uncommited.space = self.space
        form_uncommited.author = self.request.user
        form_uncommited.save()

        return super(AddDocument, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(AddDocument, self).get_context_data(**kwargs)
        space = get_object_or_404(Space, url=self.kwargs['space_url'])
        context['get_place'] = space
        return context


class EditDocument(UpdateView):

    """
    Returns a DocForm filled with the current document data.

    :permissions required: admin_space, mod_space
    :rtype: HTML Form
    :context: doc, get_place
    """
    model = Document
    template_name = 'spaces/document_form.html'

    def dispatch(self, request, *args, **kwargs):
        space = get_object_or_404(Space, url=kwargs['space_url'])

        if (request.user.has_perm('admin_space', space) or
            request.user.has_perm('mod_space', space)):
            return super(EditDocument, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

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


class DeleteDocument(DeleteView):

    """
    Returns a confirmation page before deleting the current document.

    :permissions required: admin_space, mod_space
    :rtype: Confirmation
    :context: get_place
    """
    def dispatch(self, request, *args, **kwargs):
        space = get_object_or_404(Space, url=kwargs['space_url'])
        doc = get_object_or_404(Document, pk=kwargs['doc_id'])

        if (request.user.has_perm('admin_space', space) or
            request.user.has_perm('mod_space')):
            return super(DeleteDocument, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_object(self):
        return get_object_or_404(Document, pk=self.kwargs['doc_id'])

    def get_success_url(self):
        space = self.kwargs['space_url']
        # Now we delete the file for real. It's not the best place, but here
        # we know that our user gave confirmation.
        f = get_object_or_404(Document, pk=self.kwargs['doc_id'])
        f.delete()
        return reverse(urln.SPACE_INDEX, kwargs={'space_url': space})

    def get_context_data(self, **kwargs):
        context = super(DeleteDocument, self).get_context_data(**kwargs)
        context['get_place'] = get_object_or_404(Space,
            url=self.kwargs['space_url'])
        return context


class ListDocs(ListView):

    """
    Returns a list of documents attached to the current space.

    :rtype: Object list
    :context: object_list, get_place
    """
    paginate_by = 25
    context_object_name = 'document_list'

    def dispatch(self, request, *args, **kwargs):
        space = get_object_or_404(Space, url=kwargs['space_url'])

        if request.user.has_perm('view_space', space):
            return super(ListDocs, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_queryset(self):
        place = get_object_or_404(Space, url=self.kwargs['space_url'])
        objects = Document.objects.all().filter(space=place.id) \
            .order_by('pub_date')
        return objects

    def get_context_data(self, **kwargs):
        context = super(ListDocs, self).get_context_data(**kwargs)
        context['get_place'] = get_object_or_404(Space,
            url=self.kwargs['space_url'])
        return context
