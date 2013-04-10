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
import hashlib
import datetime

from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
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
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, redirect

from apps.ecidadania.proposals import url_names as urln_prop
from core.spaces import url_names as urln_space
from core.spaces.models import Space
from apps.ecidadania.proposals.models import Proposal, ProposalSet, \
    ProposalField
from apps.ecidadania.proposals.forms import ProposalForm, VoteProposal, \
    ProposalSetForm, ProposalFieldForm, ProposalSetSelectForm, \
    ProposalMergeForm, ProposalFieldDeleteForm, ProposalFormInSet
from apps.ecidadania.debate.models import Debate


class AddProposalInSet(FormView):

    """
    Create a new single (not tied to a set) proposal.

    :parameters: space_url
    :rtype: HTML Form
    :context: form, get_place
    """
    form_class = ProposalFormInSet
    template_name = 'proposals/proposal_form_in_set.html'

    def get_success_url(self):
        space = self.kwargs['space_url']
        return reverse(urln_space.SPACE_INDEX, kwargs={'space_url': space})

    def form_valid(self, form):
        self.space = get_object_or_404(Space, url=self.kwargs['space_url'])
        pset = get_object_or_404(ProposalSet, pk=self.kwargs['set_id'])
        form_uncommited = form.save(commit=False)
        form_uncommited.space = self.space
        form_uncommited.author = self.request.user
        form_uncommited.proposalset = pset
        form_uncommited.save()
        return super(AddProposalInSet, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(AddProposalInSet, self).get_context_data(**kwargs)
        self.space = get_object_or_404(Space, url=self.kwargs['space_url'])
        self.field = ProposalField.objects.filter(proposalset=self.kwargs['set_id'])
        context['get_place'] = self.space
        context['form_field'] = [f_name.field_name for f_name in self.field]
        return context

    def dispatch(self, *args, **kwargs):
        return super(AddProposalInSet, self).dispatch(*args, **kwargs)


def add_proposal_field(request, space_url):

    """
    Adds a new form field to the proposal form. The admin can customize the proposal form for a
    particular proposal set. The optional fields will be already defined, this function will allow
    the admin to add those field to the proposal form.

    .. versionadded:: 0.1.5

    :arguments: space_url
    :context:form, get_place, prop_fields, form_data, prop_fields

    """
    form = ProposalFieldForm(request.POST or None)
    get_place = get_object_or_404(Space, url=space_url)
    if request.method == 'POST':
        if form.is_valid():
            form_data = form.save()
            proposal_fields = ProposalField.objects.filter(
                proposalset=form_data.proposalset)
            return render_to_response("proposals/proposal_add_fields.html",
                {'form_data': form_data,
                 'get_place': get_place,
                 'prop_fields': proposal_fields,
                 'form': form},
                context_instance=RequestContext(request))

    return render_to_response("proposals/proposal_add_fields.html",
        {'form': form, 'get_place': get_place},
        context_instance=RequestContext(request))


def delete_proposal_field(request, space_url):

    """
    Removes a form field from proposal form. Only for proposals which are in proposal set.

    ..versionadded:: 0.1.5

    :arguments: space_url
    :context: d_form, get_place, delete_field

    """
    d_form = ProposalFieldDeleteForm(request.POST or None)
    get_place = get_object_or_404(Space, url=space_url)
    if request.method == 'POST':
        if d_form.is_valid():
            form_data = d_form.save(commit=False)
            delete_field = ProposalField.objects.filter(
                proposalset=form_data.proposalset,
                field_name=form_data.field_name)
            delete_field.delete()
            return render_to_response(
                "proposals/proposalform_remove_field.html",
                {'form': d_form, 'get_place': get_place,
                 'deleted_field': form_data},
                context_instance=RequestContext(request))

    return render_to_response("proposals/proposalform_remove_field.html",
        {'form': d_form, 'get_place': get_place},
        context_instance=RequestContext(request))


def proposal_to_set(request, space_url):

    """
    Allows to select a proposal set to which a proposal need to be added.

    .. versionadded:: 0.1.5

    :arguments: space_url
    :context: form, get_place

    """
    get_place = get_object_or_404(Space, url=space_url)
    sel_form = ProposalSetSelectForm(request.POST or None)
    # We change here the queryset, so only the proposalsets of this space
    # appear on the list.
    sel_form.fields['proposalset'].queryset = ProposalSet.objects.filter(
        space=get_place)

    if request.method == 'POST':
        if sel_form.is_valid():
            pset = request.POST['proposalset']
            return HttpResponseRedirect(reverse(urln_prop.PROPOSAL_ADD_INSET,
                kwargs={'space_url': space_url, 'set_id': pset}))

    return render_to_response("proposals/proposalset_select_form.html",
        {'form': sel_form, 'get_place': get_place},
        context_instance=RequestContext(request))


def mergedproposal_to_set(request, space_url):

    """
    Allows to select a proposal set to which a merged proposal need to be added

    :arguments: space_url
    :context:form, get_place

    """

    sel_form = ProposalSetSelectForm(request.POST or None)
    get_place = get_object_or_404(Space, url=space_url)

    if request.method == 'POST':
        if sel_form.is_valid():
            pset = request.POST['proposalset']
            return HttpResponseRedirect(reverse(urln_prop.PROPOSAL_MERGED, kwargs={'space_url': space_url, 'set_id': pset}))

    return render_to_response("proposals/mergedproposal_in_set.html",
        {'form': sel_form, 'get_place': get_place},
        context_instance=RequestContext(request))


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
        cur_space = self.kwargs['space_url']
        place = get_object_or_404(Space, url=cur_space)
        objects = ProposalSet.objects.filter(space=place)
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
        objects = Proposal.objects.all().filter(
            proposalset=self.kwargs['set_id']).order_by('pub_date')
        return objects

    def get_context_data(self, **kwargs):
        context = super(ViewProposalSet, self).get_context_data(**kwargs)
        context['get_place'] = get_object_or_404(Space,
            url=self.kwargs['space_url'])
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
        space = self.kwargs['space_url']
        return reverse(urln_space.SPACE_INDEX, kwargs={'space_url': space})

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AddProposalSet, self).get_form_kwargs(**kwargs)
        kwargs['initial']['space'] = self.kwargs['space_url']
        return kwargs

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
        space = self.kwargs['space_url']
        pset = self.kwargs['set_id']
        return reverse(urln_prop.PROPOSALSET_VIEW, kwargs={'space_url': space,
            'set_id': pset})

    def get_object(self):
        propset_id = self.kwargs['set_id']
        return get_object_or_404(ProposalSet, pk=propset_id)

    def get_context_data(self, **kwargs):
        context = super(EditProposalSet, self).get_context_data(**kwargs)
        context['get_place'] = get_object_or_404(Space, url=self.kwargs['space_url'])
        return context

    @method_decorator(permission_required('proposals.change_proposalset'))
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
        return get_object_or_404(ProposalSet, pk=self.kwargs['set_id'])

    def get_success_url(self):
        space = self.kwargs['space_url']
        return reverse(urln_space.SPACE_INDEX, kwargs={'space_url': space})

    def get_context_data(self, **kwargs):
        context = super(DeleteProposalSet, self).get_context_data(**kwargs)
        context['get_place'] = get_object_or_404(Space, url=self.kwargs['space_url'])
        return context
