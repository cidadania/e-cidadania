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
import hashlib

from django.views.generic.detail import DetailView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.contrib import messages

from e_cidadania import settings
from core.spaces.models import Space, Intent
from helpers.cache import get_or_insert_object_in_cache
from core.permissions import has_space_permission, has_all_permissions


@login_required
def add_intent(request, space_url):

    """
    Returns a page where the logged in user can click on a "I want to
    participate" button, which after sends an email to the administrator of
    the space with a link to approve the user to use the space.
    
    :attributes:  space, intent, token
    :rtype: Multiple entity objects.
    :context: space_url, heading
    """
    space = get_object_or_404(Space, url=space_url)
    admins = space.admins.all()
    mails = []

    for m in space.admins.all():
        mails.append(m.email)

    try:
        intent = Intent.objects.get(user=request.user, space=space)
        heading = _("Access has been already authorized")
        
    except Intent.DoesNotExist:
        token = hashlib.md5("%s%s%s" % (request.user, space,
                            datetime.datetime.now())).hexdigest()
        intent = Intent(user=request.user, space=space, token=token)
        intent.save()
        subject = _("New participation request")
        body = _("User {0} wants to participate in space {1}.\n \
                Please click on the link below to approve.\n {2}").format(
                request.user.username, space.name, intent.get_approve_url())
        heading = _("Your request is being processed.")
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, mails)

    return render_to_response('space_intent.html', {'space_name': space.name,
        'heading': heading}, context_instance=RequestContext(request))


class ValidateIntent(DetailView):

    """
    Validate the user petition to join a space. This will add the user to the
    users list in the space, allowing him participation. This function checks
    if the user visiting the token url is admin of the space. If he or she is
    an admin proceeds with the validation.

    .. versionadded: 0.1.5
    """
    context_object_name = 'get_place'
    template_name = 'spaces/validate_intent.html'
    status = _("The requested intent does not exist!")

    def get_object(self):
        # Makes sure the space ins't already in the cache before hitting the
        # databass
        space_url = self.kwargs['space_url']
        space_object = get_or_insert_object_in_cache(Space, space_url, 
            url=space_url)

        if has_space_permission(self.request.user, space_object,
            allow=['admins','mods']) \
        or has_all_permissions(self.request.user):
            try:
                intent = Intent.objects.get(token=self.kwargs['token'])
                intent.space.users.add(intent.user)
                self.status = _("The user has been authorized to participate \
                in space \"%s\"." % space_object.name)
                messages.success(self.request, _("Authorization successful"))

            except Intent.DoesNotExist:
                self.status  = _("The requested intent does not exist!")

            return space_object

    def get_context_data(self, **kwargs):
        context = super(ValidateIntent, self).get_context_data(**kwargs)
        context['status'] = self.status
        context['request_user'] = Intent.objects.get(
            token=self.kwargs['token']).user
        return context