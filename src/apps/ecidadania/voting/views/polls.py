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

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.template import RequestContext
from django.contrib.auth.models import User
from django.forms.formsets import formset_factory, BaseFormSet
from django.forms.models import modelformset_factory, inlineformset_factory
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from helpers.cache import get_or_insert_object_in_cache
from django.core.urlresolvers import reverse
from django.db.models import Count, Sum

from core.spaces.models import Space
from core.spaces import url_names as urln
from apps.ecidadania.voting import url_names as urln_voting
from apps.ecidadania.voting.models import Choice, Poll
from apps.ecidadania.voting.forms import PollForm, ChoiceFormSet
from apps.ecidadania.proposals.models import Proposal


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
        queryset=Choice.objects.none())

    if (request.user.has_perm('admin_space', space) or
        request.user.has_perm('mod_space')):
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

    raise PermissionDenied


class ViewPoll(DetailView):

    """
    Display a poll. If the poll didn't start, ended, or the user already voted
    the user will be redirected to the VotePollResults view.

    ..versionadded:: 0.1.7
    """
    context_object_name = 'poll'
    template_name = 'voting/poll_detail.html'

    def dispatch(self, request, *Args, **kwargs):
        space = get_object_or_404(Space, url=kwargs['space_url'])

        if request.user.has_perm('view_space', space):
            return super(ViewPoll, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_object(self):
        poll = get_object_or_404(Poll, pk=self.kwargs['pk'])
        return poll

    def get_context_data(self, **kwargs):
        context = super(ViewPoll, self).get_context_data(**kwargs)
        context['get_place'] = get_object_or_404(Space,
            url=self.kwargs['space_url'])
        return context

    def get(self, request, **kwargs):
        self.object = self.get_object()
        if self.request.user in self.object.participants.all() \
            or datetime.date.today() >= self.object.end_date \
                or datetime.date.today() < self.object.start_date:
            return HttpResponseRedirect(reverse(urln_voting.VIEW_RESULT,
                kwargs={'space_url': self.kwargs['space_url'],
                        'pk': self.kwargs['pk']}))
        else:
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)


class ViewPollResults(DetailView):

    """
    Displays an specific poll results. The results are always available even
    after the end_date.

    .. versionadded:: 0.1.7 beta

    :context: get_place
    """
    context_object_name = 'poll'
    template_name = 'voting/poll_results.html'

    def dispatch(self, request, *Args, **kwargs):
        space = get_object_or_404(Space, url=kwargs['space_url'])

        if request.user.has_perm('view_space', space):
            return super(ViewPollResults, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_object(self):
        self.poll = get_object_or_404(Poll, pk=self.kwargs['pk'])
        return self.poll

    def get_context_data(self, **kwargs):
        context = super(ViewPollResults, self).get_context_data(**kwargs)
        space = get_object_or_404(Space, url=self.kwargs['space_url'])
        total_votes = Choice.objects.filter(poll=self.poll)

        # This fuckin' shitty logic should be removed from here, maybe there's
        # a way to do this with django. The thing is to obtain all the votes
        # from each choice and 'sum them all!'
        v = 0
        for vote in total_votes:
            v += vote.votes.count()

        context['get_place'] = space
        context['votes_total'] = v
        return context


def edit_poll(request, space_url, poll_id):

    """
    Edit a specific poll.

    :parameters: space_url, poll_id
    :context: form, get_place, choiceform, pollid
    """
    place = get_object_or_404(Space, url=space_url)

    if (request.user.has_perm('admin_space', place) or
        request.user.has_perm('mod_space', place)):

        ChoiceFormSet = inlineformset_factory(Poll, Choice, extra=1)
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

                choices = choice_form.save(commit=False)

                for form in choices:
                    form.poll = instance
                    form.save()

                return HttpResponseRedirect(reverse(urln.SPACE_INDEX,
                kwargs={'space_url': place.url}))

        return render_to_response('voting/poll_form.html',
                                 {'form': poll_form,
                                  'choiceform': choice_form,
                                  'get_place': place,
                                  'pollid': poll_id, },
                                 context_instance=RequestContext(request))
    else:
        raise PermissionDenied

class DeletePoll(DeleteView):

    """
    Delete an existent poll. Poll deletion is only reserved to spaces
    administrators or site admins.
    """
    context_object_name = "get_place"

    def dispatch(self, request, *Args, **kwargs):
        space = get_object_or_404(Space, url=kwargs['space_url'])

        if (request.user.has_perm('admin_space', space) or
            request.user.has_perm('mod_space', space)):
            return super(DeletePoll, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_success_url(self):
        space = self.kwargs['space_url']
        return '/spaces/%s' % (space)

    def get_object(self):
        space = get_object_or_404(Space, url=self.kwargs['space_url'])
        return get_object_or_404(Poll, pk=self.kwargs['poll_id'])

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

    def dispatch(self, request, *Args, **kwargs):
        space = get_object_or_404(Space, url=kwargs['space_url'])

        if request.user.has_perm('view_space', space):
            return super(ListPolls, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_queryset(self):
        key = self.kwargs['space_url']
        current_space = get_or_insert_object_in_cache(Space, key, url=key)
        polls = Poll.objects.filter(space=current_space)
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
    try:
        choice = get_object_or_404(Choice, pk=request.POST['choice'])
    except KeyError:
        return render_to_response('voting/poll_detail.html', {
            'poll': poll,
            'get_place': space,
            'error_message': "You didn't select a choice.",
        }, context_instance=RequestContext(request))

    if request.user.has_perm('view_space', space) and request.method == 'POST':
        poll.participants.add(request.user)
        choice.votes.add(request.user)
        return render_to_response('voting/poll_results.html',
            {'poll': poll, 'get_place': space, 'error_message': "You didn't \
            select a choice."}, context_instance=RequestContext(request))

    else:
        raise PermissionDenied
