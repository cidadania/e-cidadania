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

import hashlib

from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseServerError
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

    def dispatch(self, request, *Args, **kwargs):
        space = get_object_or_404(Space, url=kwargs['space_url'])

        if (request.user.has_perm('admin_space', space) or
            request.user.has_perm('mod_space', space)):
            return super(AddVoting, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

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
        form_uncommited = form.save(commit=False)
        form_uncommited.author = self.request.user
        form_uncommited.space = self.space
        form_uncommited.save()
        form.save_m2m()
        return super(AddVoting, self).form_valid(form)

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

    def dispatch(self, request, *Args, **kwargs):
        space = get_object_or_404(Space, url=kwargs['space_url'])

        if request.user.has_perm('view_space', space):
            return super(ViewVoting, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

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

    def dispatch(self, request, *Args, **kwargs):
        space = get_object_or_404(Space, url=kwargs['space_url'])

        if (request.user.has_perm('admin_space', space) or
            request.user.has_perm('mod_space', space)):
            return super(EditVoting, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_success_url(self):
        return '/spaces/' + self.space.url

    def get_object(self):
        self.space = get_object_or_404(Space, url=self.kwargs['space_url'])
        return get_object_or_404(Voting, pk=self.kwargs['voting_id'])

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

    def dispatch(self, request, *Args, **kwargs):
        space = get_object_or_404(Space, url=kwargs['space_url'])

        if (request.user.has_perm('admin_space', space) or
            request.user.has_perm('mod_space', space)):
            return super(DeleteVoting, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_success_url(self):
        space = self.kwargs['space_url']
        return '/spaces/%s' % (space)

    def get_object(self):
        self.space = get_object_or_404(Space, url=self.kwargs['space_url'])
        return get_object_or_404(Voting, pk=self.kwargs['voting_id'])

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

    def dispatch(self, request, *Args, **kwargs):
        space = get_object_or_404(Space, url=kwargs['space_url'])

        if request.user.has_perm('view_space', space):
            return super(ListVotings, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

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

    if request.user_has_perm('view_space', space):
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
                        space_absolute_url, 'voting/vote/validate/', token])
            user_email = request.user.email
            subject = _("Validate your vote")
            body = _("You voted recently on a process in our platform, please validate your vote following this link: %s") % full_url
            try:
                send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [user_email])
            except:
                return HttpResponseServerError(_("Couldn't send the email."))
        else:
            return HttpResponseBadRequest(_("Request is not POST."))
    else:
        raise PermissionDenied


def validate_voting(request, space_url, token):

    """
    Validate the votes done in a votation process. This function checks if the
    token provided by the user is the same located in the database. If the
    token is the same, a vote is added, if not, we redirect the user to an
    error page.
    """
    space = get_object_or_404(Space, url=space_url)
    tk = get_object_or_404(ConfirmVote, token=token)

    if (request.user.has_perm('admin_space', space) or
        request.user.has_perm('mod_space', space) or
        request.user == tk.user):
        try:
            prop = get_object_or_404(Proposal, pk=tk.proposal.id)
            prop.votes.add(request.user)
            return HttpResponse("Your vote has been validated.")
        except:
            return HttpResponse("Error V01: Couldn't find the token for validation or the token has already been used.")
        tk.delete()

    else:
        raise PermissionDenied
