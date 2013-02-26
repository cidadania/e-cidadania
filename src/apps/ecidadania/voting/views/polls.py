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

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.template import RequestContext
from django.views.generic.create_update import create_object
from django.views.generic.create_update import update_object
from django.contrib.auth.models import User
from django.forms.formsets import formset_factory, BaseFormSet
from django.forms.models import modelformset_factory, inlineformset_factory
from django.core.exceptions import ObjectDoesNotExist
from helpers.cache import get_or_insert_object_in_cache
from django.core.urlresolvers import reverse
from django.db.models import Count

from core.spaces.models import Space
from core.spaces import url_names as urln
from core.permissions import has_all_permissions, has_space_permission, \
    has_operation_permission
from apps.ecidadania.voting import url_names as urln_voting
from apps.ecidadania.voting.models import Choice, Poll
from apps.ecidadania.voting.forms import PollForm, ChoiceFormSet
from apps.ecidadania.proposals.models import Proposal


@permission_required('voting.add_poll')
def add_poll(request, space_url):

    """
    Create a new poll. Only registered users belonging to a concrete group
    are allowed to create polls. The polls are composed by a form and a choice
    formset.
    
    :parameters: space_url
    :context: get_place
    """
    space = get_object_or_404(Space, url=space_url)
    poll_form = PollForm(request.POST or None)
    choice_form = ChoiceFormSet(request.POST or None, prefix="choiceform",
        queryset= Choice.objects.none())

    if (has_operation_permission(request.user, space, 'voting.add_poll',
        allow=['admins', 'mods'])):
        if request.method == 'POST':
            if poll_form.is_valid() and choice_form.is_valid():
                poll_form_uncommited = poll_form.save(commit=False)
                poll_form_uncommited.space = space
                poll_form_uncommited.author = request.user

                saved_poll = poll_form_uncommited.save()
                poll_instance = get_object_or_404(Poll,
                    pk=poll_form_uncommited.pk)

                cform_uncommited = choice_form.save(commit=False)
                for cf in cform_uncommited:
                    cf.poll = poll_instance
                    cf.save()

                return HttpResponseRedirect(reverse(urln.SPACE_INDEX,
                kwargs={'space_url': space.url}))
                
        return render_to_response('voting/poll_form.html', {'form': poll_form,
            'choiceform': choice_form, 'get_place': space},
            context_instance=RequestContext(request))
    
    return render_to_response('not_allowed.html',
        context_instance=RequestContext(request))


class ViewPoll(DetailView):

    """
    Display a poll. If the poll didn't start, ended, or the user already voted
    the user will be redirected to the VotePollResults view.

    ..versionadded:: 0.1.7
    """
    context_object_name = 'poll'
    template_name = 'voting/poll_detail.html'

    def get_object(self):
        space = get_object_or_404(Space, url=self.kwargs['space_url'])
        poll = get_object_or_404(Poll, pk=self.kwargs['pk'])

        if self.request.user in poll.participants.all() \
        or datetime.date.today() >= poll.end_date \
        or datetime.date.today() <  poll.start_date:
            return HttpResponseRedirect(reverse(urln_voting.VIEW_RESULT,
                kwargs={'space_url': space.url, 'pk':poll.id}))
        else:
            return poll

    def get_context_data(self, **kwargs):
        context = super(ViewPoll, self).get_context_data(**kwargs)
        context['get_place'] = get_object_or_404(Space,
            url=self.kwargs['space_url'])
        return context


class ViewPollResults(DetailView):

    """
    Displays an specific poll results. The results are always available even
    after the end_date.

    .. versionadded:: 0.1.7 beta

    :context: get_place
    """
    context_object_name = 'poll'
    template_name = 'voting/poll_results.html'

    def get_object(self):
        poll = get_object_or_404(Poll, pk=self.kwargs['pk'])
        return poll

    def get_context_data(self, **kwargs):
        context = super(ViewPollResults, self).get_context_data(**kwargs)
        space = get_object_or_404(Space, url=self.kwargs['space_url'])
        context['get_place'] = space
        return context


def edit_poll(request, space_url, poll_id):

    """
    Edit a specific poll.

    :parameters: space_url, poll_id
    :context: form, get_place, choiceform, pollid
    """
    place = get_object_or_404(Space, url=space_url)

    if has_operation_permission(request.user, place, 'voting.change_poll',
        allow=['admins', 'mods']):
     
        ChoiceFormSet = inlineformset_factory(Poll, Choice)
        instance = Poll.objects.get(pk=poll_id)
        poll_form = PollForm(request.POST or None, instance=instance)
        choice_form = ChoiceFormSet(request.POST or None, instance=instance,
            prefix="choiceform")

        if request.method == 'POST':
            if poll_form.is_valid() and choice_form.is_valid():
                poll_form_uncommited = poll_form.save(commit=False)
                poll_form_uncommited.space = place
                poll_form_uncommited.author = request.user

                saved_poll = poll_form_uncommited.save()

                for form in choice_form.forms:
                    choice = form.save(commit=False)
                    choice.poll = instance
                    choice.save()
                return HttpResponseRedirect(reverse(urln.SPACE_INDEX,
                kwargs={'space_url': place.url}))

        return render_to_response('voting/poll_form.html',
                                 {'form': poll_form,
                                  'choiceform': choice_form,
                                  'get_place': place,
                                  'pollid': poll_id,},
                                 context_instance=RequestContext(request))
    else:
        return render_to_response('not_allowed.html',
            context_instance=RequestContext(request))


class DeletePoll(DeleteView):

    """
    Delete an existent poll. Poll deletion is only reserved to spaces
    administrators or site admins.
    """    
    context_object_name = "get_place"
    
    def get_success_url(self):
        space = self.kwargs['space_url']
        return '/spaces/%s' % (space)

    def get_object(self):
        space = get_object_or_404(Space, url=self.kwargs['space_url'])
        if has_operation_permission(self.request.user, space,
            'voting.delete_poll', allow=['admins']):
            return get_object_or_404(Poll, pk=self.kwargs['poll_id'])
        else:
            self.template_name = 'not_allowed.html'

    def get_context_data(self, **kwargs):
        context = super(DeletePoll, self).get_context_data(**kwargs)
        context['get_place'] = get_object_or_404(Space,
            url=self.kwargs['space_url'])
        return context


class ListPolls(ListView):
    """
    Return a list of polls for the current space.

    :context: get_place
    """
    paginate_by = 10

    def get_queryset(self):
        key = self.kwargs['space_url']
        current_space = get_or_insert_object_in_cache(Space, key, url=key)
        polls = Poll.objects.filter(space=current_space)

        # Here must go a validation so a user registered to the space
        # can always see the poll list. While an anonymous or not
        # registered user can't see anything unless the space is public

        return polls

    def get_context_data(self, **kwargs):
        context = super(ListPolls, self).get_context_data(**kwargs)
        key = self.kwargs['space_url']
        space = get_or_insert_object_in_cache(Space, key, url=key)
        context['get_place'] = space
        return context


def vote_poll(request, poll_id, space_url):

    """
    Vote on a choice inside the polls.

    .. versionadded:: 0.1.5
    """
    space = get_object_or_404(Space, url=space_url)
    poll = get_object_or_404(Poll, pk=poll_id)
    try :
	choice = get_object_or_404(Choice, pk=request.POST['choice'])
    except KeyError:
    	return render_to_response('voting/poll_detail.html', {
		    'poll': poll,
		    'get_place': space,
		    'error_message': "You didn't select a choice.",
		    }, context_instance=RequestContext(request))


    if request.method == 'POST' and has_space_permission(request.user, space,
    allow=['admins', 'mods', 'users']):
        poll.participants.add(request.user)
        choice.votes.add(request.user)
        return render_to_response('voting/poll_results.html',
            {'poll': poll, 'get_place': space, 'error_message': "You didn't \
            select a choice."}, context_instance=RequestContext(request))

    else:
        return HttpResponse("Error P02: Couldn't emit the vote. You're not \
            allowed.")
