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

import datetime

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.template import RequestContext
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from apps.ecidadania.staticpages.models import StaticPage


@permission_required('staticpages.add_staticpage')
def add_page(request, slug):

    """
    This function goes into the administration
    """
    pass


class ViewPage(DetailView):

    """
    Get the request page and view it. There are no view restrictions on views.
    """
    context_object_name = 'staticpage'
    template_name = 'staticpages/staticpages_index.html'

    def get_object(self):
        self.page = get_object_or_404(StaticPage, uri=self.kwargs['slug'])
        return self.page


class EditPage(UpdateView):

    """
    """
    model = StaticPage
    template_name = 'staticpages/staticpages_edit.html'
    success_url = '/'

    def get_object(self):
        self.page = get_object_or_404(StaticPage, uri=self.kwargs['slug'])
        return self.page

#    def get_context_data(self, **kwargs):
#        context = super(EditPage, self).get_context_data(**kwargs)
#        context['get_place'] = get_object_or_404(Space, url=self.kwargs['space_name'])
#        return context

    @method_decorator(permission_required('staticpages.change_staticpage'))
    def dispatch(self, *args, **kwargs):
        return super(EditPage, self).dispatch(*args, **kwargs)


class DeletePage(DeleteView):

    """
    """
    sucess_url = '/'

    def get_object(self):
        return get_object_or_404(StaticPage, uri=self.kwargs['slug'])

    @method_decorator(permission_required('staticpages.delete_staticpage'))
    def dispatch(self, *args, **kwargs):
        return super(DeletePage, self).dispatch(*args, **kwargs)
