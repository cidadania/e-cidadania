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
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object, update_object
from django.views.generic.create_update import delete_object

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
