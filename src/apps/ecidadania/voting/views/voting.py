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

import hashlib

from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic.base import TemplateView, RedirectView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic import FormView
from django.template import RequestContext
from django.views.generic.create_update import create_object
from django.views.generic.create_update import update_object
from django.contrib.auth.models import User
from django.forms.formsets import formset_factory, BaseFormSet
from django.forms.models import modelformset_factory, inlineformset_factory
from django.core.exceptions import ObjectDoesNotExist
from helpers.cache import get_or_insert_object_in_cache
from django.core.urlresolvers import NoReverseMatch, reverse
from django.template.response import TemplateResponse
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import get_current_site

from e_cidadania import settings
from core.spaces.models import Space
from core.permissions import has_all_permissions, has_space_permission, has_operation_permission
from apps.ecidadania.voting.models import *
from apps.ecidadania.voting.forms import *
from apps.ecidadania.proposals.models import Proposal, ProposalSet


class AddVoting(FormView):

    """
    Create a new voting process. Only registered users belonging to a concrete
    group are allowed to create voting processes.

    versionadded: 0.1

    :parameters: space_url
    :context: get_place
    """
    form_class = VotingForm
    template_name = 'voting/voting_form.html'

    def get_form_kwargs(self):
        """
        This send the current space to the form so we can change the
        foreignkeys querysets there.
        """
        space = get_object_or_404(Space, url=self.kwargs['space_url'])
        kwargs = super(AddVoting, self).get_form_kwargs()
        kwargs['current_space'] = space 
        return kwargs

    def get_success_url(self):
        self.space = get_object_or_404(Space, url=self.kwargs['space_url'])
        return '/spaces/' + self.space.url + '/'

    def form_valid(self, form):
        self.space = get_object_or_404(Space, url=self.kwargs['space_url'])
        if has_operation_permission(self.request.user, self.space, 'voting.add_voting', allow=['admins', 'mods']):
            form_uncommited = form.save(commit=False)
            form_uncommited.author = self.request.user
            form_uncommited.space = self.space
            form_uncommited.save()
            form.save_m2m()
            return super(AddVoting, self).form_valid(form)
        else:
            template_name = 'not_allowed.html'


    def get_context_data(self, **kwargs):
        context = super(AddVoting, self).get_context_data(**kwargs)
        self.space = get_object_or_404(Space, url=self.kwargs['space_url'])
        context['get_place'] = self.space
        return context


class ViewVoting(DetailView):

    """
    View a specific voting process.

    Proposals: Return unlinked proposals (not linked to sets)
    All_proposals
    """
    context_object_name = 'voting'
    template_name = 'voting/voting_detail.html'

    def get_object(self):
        return Voting.objects.get(pk=self.kwargs['voting_id'])

    def get_context_data(self, **kwargs):

        """
        Get extra context data for the ViewVoting view.
        """
        context = super(ViewVoting, self).get_context_data(**kwargs)
        context['get_place'] = get_object_or_404(Space, url=self.kwargs['space_url'])
        voting = Voting.objects.get(pk=self.kwargs['voting_id'])
        all_proposals = Proposal.objects.all()
        proposalsets = voting.proposalsets.all()
        proposals = voting.proposals.all()
        print "proposalsets: %s" % proposalsets
        print "proposals: %s" % proposals
        print "all_proposals: %s" % all_proposals
        print "prop inside set: %s" % Proposal.objects.filter(proposalset=proposalsets)
        context['proposalsets'] = proposalsets
        context['proposals'] = proposals
        context['all_proposals'] = all_proposals

        return context


class EditVoting(UpdateView):

    """
    Edit an existent voting process.

    :parameters: space_url, voting_id
    :context: get_place
    """
    model = Voting
    template_name = 'voting/voting_form.html'

    def get_success_url(self):
        return '/spaces/' + self.space.url

    def get_object(self):
        self.space = get_object_or_404(Space, url=self.kwargs['space_url'])
        if has_operation_permission(self.request.user, self.space, 'voting.change_voting', allow=['admins', 'mods']):
            return get_object_or_404(Voting, pk=self.kwargs['voting_id'])
        else:
            self.template_name = 'not_allowed.html'

    def get_context_data(self, **kwargs):
        context = super(EditVoting, self).get_context_data(**kwargs)
        context['get_place'] = self.space
        return context


class DeleteVoting(DeleteView):

    """
    Delete an existent voting process. Voting process deletion is only reserved to spaces
    administrators or site admins.
    """
    context_object_name = "get_place"

    def get_success_url(self):
        space = self.kwargs['space_url']
        return '/spaces/%s' % (space)

    def get_object(self):
        self.space = get_object_or_404(Space, url=self.kwargs['space_url'])
        if has_operation_permission(self.request.user, self.space, 'voting.delete_voting', allow=['admins', 'mods']):
            return get_object_or_404(Voting, pk=self.kwargs['voting_id'])
        else:
            self.template_name = 'not_allowed.html'

    def get_context_data(self, **kwargs):

        """
        Get extra context data for the ViewVoting view.
        """
        context = super(DeleteVoting, self).get_context_data(**kwargs)
        context['get_place'] = self.space
        return context

class ListVotings(ListView):

    """
    List all the existing votings inside the space. This is meant to be a
    tabbed view, just like the spaces list. The user can see the open and
    closed votings.

    .. versionadded:: 0.1.7 beta
    """
    paginate_by = 10

    def get_queryset(self):
        key = self.kwargs['space_url']
        current_space = get_or_insert_object_in_cache(Space, key, url=key)
        votings = Voting.objects.filter(space=current_space)
        return votings

    def get_context_data(self, **kwargs):
        context = super(ListVotings, self).get_context_data(**kwargs)
        key = self.kwargs['space_url']
        space = get_or_insert_object_in_cache(Space, key, url=key)
        context['get_place'] = space
        return context


def vote_voting(request, space_url):

    """
    View to control the votes during a votation process. Do not confuse with
    proposals support_votes. This function creates a new ConfirmVote object
    trough VoteForm with the user and a token. After that an email is sent
    to the user with the token for validation. This function does not add the
    votes.

    .. versionadded:: 0.1.7
    """
    proposal = get_object_or_404(Proposal, pk=request.POST['propid'])
    space = get_object_or_404(Space, url=space_url)
    voteform = VoteForm(request.POST)

    if has_operation_permission(request.user, space,'voting.change_voting', allow=['admins', 'mods',
        'users']):
        if request.method == 'POST' and voteform.is_valid():
            # Generate the objetct
            token = hashlib.md5("%s%s%s" % (request.user, space,
                        datetime.datetime.now())).hexdigest()
            voteform_uncommitted = voteform.save(commit=False)
            voteform_uncommitted.user = request.user
            voteform_uncommitted.token = token
            voteform_uncommitted.proposal = proposal
            voteform_uncommitted.save()

            # Send the email to the user. Get URL, get user mail, send mail.
            space_absolute_url = space.get_absolute_url()
            full_url = ''.join(['http://', get_current_site(request).domain,
                        space_absolute_url, 'vote/validate/', token])
            user_email = request.user.email
            subject = _("Validate your vote")
            body = _("You voted recently on a process in our platform, please validate your vote following this link: %s") % full_url
            send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [user_email])

            return HttpResponse("Vote emmited")

    else:
        return HttpResponse("Error P02: Couldn't emit the vote. You're not \
            allowed.")

def validate_voting(request, token):

    """
    Validate the votes done in a votation process. This function checks if the
    token provided by the user is the same located in the database. If the
    token is the same, a vote is added, if not, we redirect the user to an
    error page.
    """
    space = get_object_or_404(Space, url=space_url)
    voting = get_object_or_404(Voting, pk=voting_id)
    try:
        token = ConfirmVote.object.get(token=token)
    except:
        return HttpResponse("Couldn't find the token for validation.")
