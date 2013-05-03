# -*- coding: utf-8 -*-
#
# Copyright (c) 2010-2013 Cidadania S. Coop. Galega
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
from django.views.generic.detail import DetailView
from django.views.generic import FormView
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from guardian.shortcuts import assign_perm

from core.spaces import url_names as urln
from core.spaces.models import Space, Event
from core.spaces.forms import SpaceForm, EventForm
from helpers.cache import get_or_insert_object_in_cache


class AddEvent(FormView):

    """
    Returns an empty MeetingForm to create a new Meeting. Space and author
    fields are automatically filled with the request data.

    :permissions required: admin_space, mod_space
    :rtype: HTML Form
    :context: form, get_place
    """
    form_class = EventForm
    template_name = 'spaces/event_form.html'

    def dispatch(self, request, *args, **kwargs):
        space = get_object_or_404(Space, url=kwargs['space_url'])

        if (request.user.has_perm('admin_space', space) or
            request.user.has_perm('mod_space', space)):
            return super(AddEvent, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_success_url(self):
        space = self.kwargs['space_url']
        return reverse(urln.SPACE_INDEX, kwargs={'space_url': space})

    def form_valid(self, form):
        self.space = get_object_or_404(Space, url=self.kwargs['space_url'])
        form_uncommited = form.save(commit=False)
        form_uncommited.event_author = self.request.user
        form_uncommited.space = self.space
        form_uncommited.save()
        form.save_m2m()

        # Assign all the permissions
        assign_perm('view_event', self.request.user, self.space)
        assign_perm('change_event', self.request.user, self.space)
        assign_perm('delete_event', self.request.user, self.space)
        assign_perm('admin_event', self.request.user, self.space)

        return super(AddEvent, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(AddEvent, self).get_context_data(**kwargs)
        place = get_object_or_404(Space, url=self.kwargs['space_url'])
        context['get_place'] = place
        context['user_is_admin'] = (has_space_permission(self.request.user,
            place, allow=['admins', 'mods']) or has_all_permissions(
                self.request.user))
        return context


class ViewEvent(DetailView):

    """
    View the content of a event.

    :permissions required: view_space
    :rtype: Object
    :context: event, get_place
    """
    context_object_name = 'event'
    template_name = 'spaces/event_detail.html'

    def dispatch(self, request, *args, **kwargs):
        space = get_object_or_404(Space, url=kwargs['space_url'])

        if request.user.has_perm('view_space', space):
            return super(ViewEvent, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_object(self):
        return get_object_or_404(Event, pk=self.kwargs['event_id'])

    def get_context_data(self, **kwargs):
        context = super(ViewEvent, self).get_context_data(**kwargs)
        context['get_place'] = get_object_or_404(Space,
            url=self.kwargs['space_url'])
        return context


class EditEvent(UpdateView):

    """
    Returns a MeetingForm filled with the current Meeting data to be edited.

    :permissions required: admin_space, admin_event, mod_space, change_event
    :rtype: HTML Form
    :context: event, get_place
    """
    model = Event
    template_name = 'spaces/event_form.html'

    def dispatch(self, request, *args, **kwargs):
        space = get_object_or_404(Space, url=kwargs['space_url'])
        event = get_object_or_404(Event, pk=kwargs['event_id'])

        if (request.user.has_perm('admin_space', space) or
            request.user.has_perm('mod_space', space) or
            (request.user.has_perm('admin_event', event) and
             request.user.has_perm('change_event', event))):
            return super(EditEvent, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_object(self):
        cur_event = get_object_or_404(Event, pk=self.kwargs['event_id'])
        return cur_event

    def get_success_url(self):
        space = self.kwargs['space_url']
        return reverse(urln.SPACE_INDEX, kwargs={'space_url': space})

    def form_valid(self, form):
        form_uncommited = form.save(commit=False)
        form_uncommited.save()
        form.save_m2m()

        return super(EditEvent, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(EditEvent, self).get_context_data(**kwargs)
        space = get_object_or_404(Space, url=self.kwargs['space_url'])
        context['get_place'] = space
        context['user_is_admin'] = (has_space_permission(self.request.user,
            space, allow=['admins', 'mods']) or has_all_permissions(
                self.request.user))
        return context


class DeleteEvent(DeleteView):

    """
    Returns a confirmation page before deleting the Meeting object.

    :permissions required: admin_space, mod_space, admin_event, delete_event
    :rtype: Confirmation
    :context: get_place
    """

    def dispatch(self, request, *args, **kwargs):
        space = get_object_or_404(Space, url=kwargs['space_url'])
        event = get_object_or_404(Event, url=kwargs['event_id'])

        if (request.user.has_perm('admin_space', space) or
            request.user.has_perm('mod_space'), space or
            (request.user.has_perm('admin_event', event) and
             request.user.has_perm('delete_event', event))):
            return super(DeleteEvent, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_object(self):
        return get_object_or_404(Event, pk=self.kwargs['event_id'])

    def get_success_url(self):
        space = self.kwargs['space_url']
        return reverse(urln.SPACE_INDEX, kwargs={'space_url': space})

    def get_context_data(self, **kwargs):
        context = super(DeleteEvent, self).get_context_data(**kwargs)
        context['get_place'] = get_object_or_404(Space,
            url=self.kwargs['space_url'])
        return context


class ListEvents(ListView):

    """
    List all the events attached to a space.

    :permissions required: view_space
    :rtype: Object list
    :context: event_list, get_place
    """
    paginate_by = 25
    context_object_name = 'event_list'

    def dispatch(self, request, *args, **kwargs):
        space = get_object_or_404(Space, url=kwargs['space_url'])
        if request.user.has_perm('view_space', space):
            return super(ListEvents, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_queryset(self):
        place = get_object_or_404(Space, url=self.kwargs['space_url'])
        objects = Event.objects.all().filter(space=place.id).order_by('event_date')
        return objects

    def get_context_data(self, **kwargs):
        context = super(ListEvents, self).get_context_data(**kwargs)
        context['get_place'] = get_object_or_404(Space,
            url=self.kwargs['space_url'])
        return context
