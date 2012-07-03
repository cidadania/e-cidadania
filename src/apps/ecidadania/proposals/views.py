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

"""
Proposal module views.
"""

# Generic class-based views
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic import FormView
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.template import RequestContext
from django.views.decorators.http import require_POST
from django.db.models import Count
from django.utils.decorators import method_decorator
from django.views.generic.create_update import update_object
from django.db.models import F
from django.http import HttpResponse

from apps.ecidadania.proposals.models import Proposal, ProposalSet
from apps.ecidadania.proposals.forms import ProposalForm, VoteProposal, \
     ProposalSetForm
from core.spaces.models import Space


class AddProposal(FormView):

    """
    Create a new proposal.
    
    :parameters: space_url
    :rtype: HTML Form
    :context: form, get_place
    """
    form_class = ProposalForm
    template_name = 'proposals/proposal_form.html'
    
    def get_success_url(self):
        return '/spaces/' + self.kwargs['space_url']
    
    def form_valid(self, form):
        self.space = get_object_or_404(Space, url=self.kwargs['space_url'])
        form_uncommited = form.save(commit=False)
        form_uncommited.space = self.space
        form_uncommited.author = self.request.user
        form_uncommited.save()
        return super(AddProposal, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(AddProposal, self).get_context_data(**kwargs)
        self.space = get_object_or_404(Space, url=self.kwargs['space_url'])
        context['get_place'] = self.space
        return context
        
    @method_decorator(permission_required('proposals.add_proposal'))
    def dispatch(self, *args, **kwargs):
        return super(AddProposal, self).dispatch(*args, **kwargs)


class ViewProposal(DetailView):

    """
    Detail view of a proposal. Inherits from django :class:`DetailView` generic
    view.

    :rtype: object
    :context: proposal
    """
    context_object_name = 'proposal'
    template_name = 'proposals/proposal_detail.html'

    def get_object(self):
        prop_id = self.kwargs['prop_id']
        return get_object_or_404(Proposal, pk = prop_id)

    def get_context_data(self, **kwargs):
        context = super(ViewProposal, self).get_context_data(**kwargs)
        current_space = get_object_or_404(Space, url=self.kwargs['space_url'])
        support_votes_count = Proposal.objects.filter(space=current_space)\
                             .annotate(Count('support_votes'))
        # We are going to get the proposal position in the list
        self.get_position = 0
        for i,x in enumerate(support_votes_count):
            if x.id == int(self.kwargs['prop_id']):
                self.get_position = i
        context['get_place'] = current_space
        context['support_votes_count'] = support_votes_count[int(self.get_position)].support_votes__count
        return context


class EditProposal(UpdateView):

    """
    The proposal can be edited by space and global admins, but also by their
    creator.

    :rtype: HTML Form
    :context: get_place
    :parameters: space_url, prop_id
    """
    model = Proposal
    template_name = 'proposals/proposal_form.html'
    
    def get_success_url(self):
        return '/spaces/{0}/proposal/{1}/'.format(self.kwargs['space_url'], self.kwargs['prop_id'])
        
    def get_object(self):
        prop_id = self.kwargs['prop_id']
        return get_object_or_404(Proposal, pk = prop_id)
        
    def get_context_data(self, **kwargs):
        context = super(EditProposal, self).get_context_data(**kwargs)
        context['get_place'] = get_object_or_404(Space, url=self.kwargs['space_url'])
        return context
        
    @method_decorator(permission_required('proposals.edit_proposal'))
    def dispatch(self, *args, **kwargs):
        return super(EditProposal, self).dispatch(*args, **kwargs)
                             
            
class DeleteProposal(DeleteView):

    """
    Delete a proposal.

    :rtype: Confirmation
    :context: get_place
    """
    def get_object(self):
        return get_object_or_404(Proposal, pk = self.kwargs['prop_id'])

    def get_success_url(self):
        current_space = self.kwargs['space_url']
        return '/spaces/{0}'.format(current_space)

    def get_context_data(self, **kwargs):
        context = super(DeleteProposal, self).get_context_data(**kwargs)
        context['get_place'] = get_object_or_404(Space, url=self.kwargs['space_url'])
        return context                 
                  
           
@require_POST
def vote_proposal(request, space_url):

    """
    Increment support votes for the proposal in 1.
    """
    prop = get_object_or_404(Proposal, pk=request.POST['propid'])
#    if Proposal.objects.filter(support_votes__contains=request.user):
#        return HttpResponse("You already voted")
#    else:
    prop.support_votes.add(request.user)
    return HttpResponse("Vote emmited.")


class ListProposals(ListView):

    """
    List all proposals stored whithin a space. Inherits from django :class:`ListView`
    generic view.

    :rtype: Object list
    :context: proposal
    """
    paginate_by = 50
    context_object_name = 'proposal'

    def get_queryset(self):
        place = get_object_or_404(Space, url=self.kwargs['space_url'])
        objects = Proposal.objects.annotate(Count('support_votes')).filter(space=place.id).order_by('pub_date')
        return objects

    def get_context_data(self, **kwargs):
        context = super(ListProposals, self).get_context_data(**kwargs)
        context['get_place'] = get_object_or_404(Space, url=self.kwargs['space_url'])
        return context

#
# Proposal Sets
#

class ListProposalSet(ListView):

    """
    List all the proposal set in a space.
    
    .. versionadded: 0.1.5
    
    :rtype: Object list
    :context: setlist
    """
    paginate_by = 20
    context_object_name = 'setlist'
    
    def get_queryset(self):
        place = get_object_or_404(Space, url=self.kwargs['space_url'])
        objects = ProposalSet.objects.all()
        return objects
    
    def get_context_data(self, **kwargs):
        context = super(ListProposalSet, self).get_context_data(**kwargs)
        context['get_place'] = get_object_or_404(Space, url=self.kwargs['space_url'])
        return context
    
class ViewProposalSet(ListView):

    """
    List all the proposals inside a proposals set.
    
    .. versionadded 0.1.5
    
    :rtype: Object list
    :context: proposalset
    """
    paginate_by = 50
    context_object_name = 'proposalset'
    template_name = 'proposals/proposalset_detail.html'
    
    def get_queryset(self):
        place = get_object_or_404(Space, url=self.kwargs['space_url'])
        objects = Proposal.objects.all().filter(proposalset=self.kwargs['set_id']).order_by('pub_date')
        return objects
    
    def get_context_data(self, **kwargs):
        context = super(ViewProposalSet, self).get_context_data(**kwargs)
        context['get_place'] = get_object_or_404(Space, url=self.kwargs['space_url'])
        return context

class AddProposalSet(FormView):

    """
    Create a new prpoposal set, it can be related to a debate or be in free mode,
    which is not linked to anything. If it's linked to a debate, people can
    make their proposals related to the debate notes.
    
    .. versionadded: 0.1.5
    
    :rtype: Form object
    :context: form, get_place
    """
    form_class = ProposalSetForm
    template_name = 'proposals/proposalset_form.html'
    
    def get_success_url(self):
        return '/spaces/' + self.kwargs['space_url']
    
    def form_valid(self, form):
        self.space = get_object_or_404(Space, url=self.kwargs['space_url'])
        form_uncommited = form.save(commit=False)
        form_uncommited.space = self.space
        form_uncommited.author = self.request.user
        form_uncommited.save()
        return super(AddProposalSet, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(AddProposalSet, self).get_context_data(**kwargs)
        self.space = get_object_or_404(Space, url=self.kwargs['space_url'])
        context['get_place'] = self.space
        return context
        
    @method_decorator(permission_required('proposals.add_proposalset'))
    def dispatch(self, *args, **kwargs):
        return super(AddProposalSet, self).dispatch(*args, **kwargs)
        
class EditProposalSet(UpdateView):

    """
    Modify an already created proposal set.
    
    .. versionadded: 0.1.5
    
    :rtype: Form object
    :context: form, get_place
    """
    model = ProposalSet
    template_name = 'proposals/proposalset_form.html'
    
    def get_success_url(self):
        return '/spaces/{0}/proposal/psets/{1}/'.format(self.kwargs['space_url'], self.kwargs['set_id'])
        
    def get_object(self):
        propset_id = self.kwargs['set_id']
        return get_object_or_404(ProposalSet, pk = propset_id)
        
    def get_context_data(self, **kwargs):
        context = super(EditProposalSet, self).get_context_data(**kwargs)
        context['get_place'] = get_object_or_404(Space, url=self.kwargs['space_url'])
        return context
        
    @method_decorator(permission_required('proposals.edit_proposalset'))
    def dispatch(self, *args, **kwargs):
        return super(EditProposalSet, self).dispatch(*args, **kwargs)

class DeleteProposalSet(DeleteView):

    """
    Delete a proposal set.
    
    .. versionadded: 0.1.5
    
    :rtype: Confirmation
    :context: get_place
    """
    def get_object(self):
        return get_object_or_404(ProposalSet, pk = self.kwargs['set_id'])

    def get_success_url(self):
        current_space = self.kwargs['space_url']
        return '/spaces/{0}'.format(current_space)

    def get_context_data(self, **kwargs):
        context = super(DeleteProposalSet, self).get_context_data(**kwargs)
        context['get_place'] = get_object_or_404(Space, url=self.kwargs['space_url'])
        return context                 
