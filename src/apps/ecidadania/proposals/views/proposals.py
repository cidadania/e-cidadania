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

from django.core.urlresolvers import reverse
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic import FormView
from django.views.generic.create_update import update_object
from django.views.decorators.http import require_POST
from django.db.models import Count
from django.db.models import F
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, redirect

from apps.ecidadania.proposals import url_names as urln_prop
from core.spaces import url_names as urln_space
from core.spaces.models import Space
from core.permissions import has_operation_permission, has_space_permission
from apps.ecidadania.proposals.models import Proposal, ProposalSet, \
        ProposalField
from apps.ecidadania.proposals.forms import ProposalForm, VoteProposal, \
        ProposalSetForm, ProposalFieldForm, ProposalSetSelectForm, \
        ProposalMergeForm, ProposalFieldDeleteForm

class AddProposal(FormView):

    """
    Create a new single (not tied to a set) proposal. The permission checks are
    done in the form_valid method.
    
    :parameters: space_url
    :rtype: HTML Form
    :context: form, get_place
    """
    form_class = ProposalForm
    template_name = 'proposals/proposal_form.html'
    
    def get_success_url(self):
        space = self.kwargs['space_url']
        return reverse(urln_space.SPACE_INDEX, kwargs={'space_url':space})
        
    def form_valid(self, form):
        space = get_object_or_404(Space, url=self.kwargs['space_url'])

        if has_operation_permission(self.request.user, space,
        'proposals.add_proposal', allow=['admins', 'mods','users']):
            form_uncommited = form.save(commit=False)
            form_uncommited.space = space
            form_uncommited.author = self.request.user
            form_uncommited.save()

            return super(AddProposal, self).form_valid(form)
        else:
            return render_to_response('not_allowed.html',
                context_instance=RequestContext(self.request))
    
    def get_context_data(self, **kwargs):
        context = super(AddProposal, self).get_context_data(**kwargs)
        self.space = get_object_or_404(Space, url=self.kwargs['space_url'])
        #self.field = ProposalField.objects.filter(proposalset=self.kwargs['p_set'])
        context['get_place'] = self.space
        #context['form_field'] = [f_name.field_name for f_name in self.field]
        return context
    
    @method_decorator(permission_required('proposals.add_proposal'))
    def dispatch(self, *args, **kwargs):
        return super(AddProposal, self).dispatch(*args, **kwargs)


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
        space = self.kwargs['space_url']
        proposal = self.kwargs['prop_id']
        return reverse(urln_prop.PROPOSAL_VIEW, kwargs={'space_url':space,
                                                        'prop_id':proposal})
        
    def get_object(self):
        prop_id = self.kwargs['prop_id']
        space_url = self.kwargs['space_url']
        proposal = get_object_or_404(Proposal, pk = prop_id)
        space = get_object_or_404(Space, url = space_url)

        if has_operation_permission(self.request.user, space,
        'proposals.change_proposal', allow=['admins', 'mods']) \
        or proposal.author.id == self.request.user.id:
            return get_object_or_404(Proposal, pk = prop_id)
        else:
            return render_to_response('not_allowed.html',
                context_instance=RequestContext(self.request))
        
    def get_context_data(self, **kwargs):
        context = super(EditProposal, self).get_context_data(**kwargs)
        self.p_set = Proposal.objects.get(pk = self.kwargs['prop_id'])
        self.field = ProposalField.objects.filter(proposalset = self.p_set.proposalset)
        context['form_field'] = [f_name.field_name for f_name in self.field]
        context['get_place'] = get_object_or_404(Space, url=self.kwargs['space_url'])
        return context
        
    @method_decorator(permission_required('proposals.change_proposal'))
    def dispatch(self, *args, **kwargs):
        return super(EditProposal, self).dispatch(*args, **kwargs)


class DeleteProposal(DeleteView):

    """
    Delete a proposal.

    :rtype: Confirmation
    :context: get_place
    """
    def get_object(self):
        prop_id = self.kwargs['prop_id']
        space_url = self.kwargs['space_url']
        proposal = get_object_or_404(Proposal, pk = prop_id)
        space = get_object_or_404(Space, url = space_url)

        if has_operation_permission(self.request.user, space,
        'proposals.delete_proposal', allow=['admins', 'mods']) \
        or proposal.author.id == self.request.user.id:
            return proposal
        else:
            return render_to_response('not_allowed.html',
                context_instance=RequestContext(self.request))

    def get_success_url(self):
        space = self.kwargs['space_url']
        return reverse(urln_space.SPACE_INDEX, kwargs={'space_url':space})

    def get_context_data(self, **kwargs):
        context = super(DeleteProposal, self).get_context_data(**kwargs)
        context['get_place'] = get_object_or_404(Space, url=self.kwargs['space_url'])
        return context

    @method_decorator(permission_required('proposal.delete_proposal'))
    def dispatch(self, *args, **kwargs):
        return super(DeleteProposal, self).dispatch(*args, **kwargs)


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

        if place.public or has_space_permission(self.request.user, place,
            allow=['admins', 'mods', 'users']):
            return objects
        else:
            return render_to_response('not_allowed.html',
                context_instance=RequestContext(self.request))

    def get_context_data(self, **kwargs):
        context = super(ListProposals, self).get_context_data(**kwargs)
        context['get_place'] = get_object_or_404(Space, url=self.kwargs['space_url'])   
        return context

def merge_proposal(request, space_url, set_id):
    
    """
    Create a new merged proposal. This proposal can be linked to many other proposals which are in the
    same proposal set. Only admin and moderator can create merged proposals.

    .. versionadded:: 0.1.5

    :arguments: space_url, p_set
    :context:form, get_place, form_field

    """
    get_place = get_object_or_404(Space, url=space_url)
    field = ProposalField.objects.filter(proposalset=set_id)
    form_field = [f_name.field_name for f_name in field]

    if request.method == 'POST' and has_space_permission(request.user, get_place, allow=['admins', 'mods', 'users']):
        merged_form = ProposalForm(request.POST)
        if merged_form.is_valid():
            form_data = merged_form.save(commit=False)
            form_data.proposalset = get_object_or_404(ProposalSet, pk=set_id)
            form_data.space = get_object_or_404(Space, url=space_url)
            form_data.author = request.user
            form_data.merged = True
            field = ProposalField.objects.filter(proposalset=set_id)
            form_field = [f_name.field_name for f_name in field]
            form_data.save()
            merged_form.save_m2m()

            return reverse(urln_space.SPACE_INDEX,
                kwargs={'space_url':space_url})
    else:
        print "id: " + set_id
        merged_form = ProposalMergeForm(initial={'set_id':set_id})

    return render_to_response("proposals/proposal_merged.html",
        {'form':merged_form, 'get_place':get_place, 'form_field':form_field},
        context_instance = RequestContext(request))