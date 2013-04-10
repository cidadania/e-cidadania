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
Common functions and classes for proposals and proposal sets.
"""

from django.views.generic.detail import DetailView
from django.views.decorators.http import require_POST
from django.db.models import Count
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from apps.ecidadania.proposals import url_names as urln_prop
from core.spaces import url_names as urln_space
from core.spaces.models import Space
from core.permissions import has_space_permission, has_all_permissions, has_operation_permission
from apps.ecidadania.proposals.models import Proposal


class ViewProposal(DetailView):

    """
    Detail view of a proposal. Inherits from django :class:`DetailView` generic
    view.

    **Permissions:** Everyone can read if the space is public. If it is private
    only logged in users that belong to any of the space groups can read. In
    other case just return an empty object and a not_allowed template.

    :rtype: object
    :context: proposal
    """
    context_object_name = 'proposal'
    template_name = 'proposals/proposal_detail.html'

    def get_object(self):
        prop_id = self.kwargs['prop_id']
        space_url = self.kwargs['space_url']
        proposal = get_object_or_404(Proposal, pk=prop_id)
        place = get_object_or_404(Space, url=space_url)

        if place.public:
            return proposal
        elif has_space_permission(self.request.user, place,
            allow=['admins', 'mods', 'users']) \
                or has_all_permissions(self.request.user):
            return proposal
        else:
            self.template_name = 'not_allowed.html'
            return Proposal.objects.none()

    def get_context_data(self, **kwargs):
        context = super(ViewProposal, self).get_context_data(**kwargs)
        current_space = get_object_or_404(Space, url=self.kwargs['space_url'])
        # We are going to get the proposal position in the list
        self.get_position = 0
        proposal = get_object_or_404(Proposal, pk=self.kwargs['prop_id'])
        if proposal.merged:
            context['merged_proposal'] = proposal.merged_proposals.all()

        support_votes_count = Proposal.objects.filter(space=current_space)\
                             .annotate(Count('support_votes'))
        for i, x in enumerate(support_votes_count):
            if x.id == int(self.kwargs['prop_id']):
                self.get_position = i
        context['support_votes_count'] = support_votes_count[int(self.get_position)].support_votes__count
        context['get_place'] = current_space
        return context


@require_POST
def support_proposal(request, space_url):

    """
    Increment support votes for the proposal in 1. We porform some permission
    checks, for example, the user has to be inside any of the user groups of
    the space.
    """
    prop = get_object_or_404(Proposal, pk=request.POST['propid'])
    space = get_object_or_404(Space, url=space_url)

    if has_operation_permission(request.user, space,
    "proposals.change_proposal", allow=['admins', 'mods', 'users']):
        try:
            prop.support_votes.add(request.user)
            return HttpResponse(" Support vote emmited.")
        except:
            return HttpResponse("Error P01: Couldn't emit the vote. Couldn't \
                add the user to the count. Contact support and tell them the \
                error code.")
    else:
        return HttpResponse("Error P02: Couldn't emit the vote. You're not \
            allowed.")

# @require_POST
# def vote_proposal(request, space_url):

#     """
#     Send email to user to validate vote before is calculated.
#     :attributes: - prop: current proposal
#     :rtype: multiple entity objects.
#     """
#     prop = get_object_or_404(Proposal, pk=request.POST['propid'])
#     try:
#          intent = ConfirmVote.objects.get(user=request.user, proposal=prop)
#     except ConfirmVote.DoesNotExist:
#         token = hashlib.md5("%s%s%s" % (request.user, prop,
#                             datetime.datetime.now())).hexdigest()
#         intent = ConfirmVote(user=request.user, proposal=prop, token=token)
#         intent.save()
#         subject = _("New vote validation request")
#         body = _("Hello {0}, \n \
#                  You are getting this email because you wanted to support proposal {1}.\n\
#                  Please click on the link below to vefiry your vote.\n {2} \n \
#                  Thank you for your vote."
#                  .format(request.user.username, prop.title,
#                  intent.get_approve_url()))
#         send_mail(subject=subject, message=body,
#                    from_email="noreply@ecidadania.org",
#                    recipient_list=[request.user.email])
