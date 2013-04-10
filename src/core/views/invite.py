#/usr/bin/env python
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

from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.shortcuts import render_to_response
from django.template import RequestContext, loader, Context
from django.utils.translation import ugettext_lazy as _
from e_cidadania import settings


def invite(request):

    """
    Simple view to send invitations to friends via mail. Making the invitation
    system as a view, guarantees that no invitation will be monitored or saved
    to the hard disk.
    """
    if request.method == "POST":
        mail_addr = request.POST['email_addr']
        raw_addr_list = mail_addr.split(',')
        addr_list = [x.strip() for x in raw_addr_list]
        usr_msg = request.POST['mail_msg']

        plain_template = "invite/invite_plain.txt"
        html_template = "invite/invite.html"

        plain_msg = loader.get_template(plain_template).render(
            RequestContext(request,
                                                {'msg': usr_msg}))
        html_msg = loader.get_template(html_template).render(
            RequestContext(request,
                                                {'msg': usr_msg}))

        email = EmailMultiAlternatives(_('Invitation to join e-cidadania'), plain_msg, settings.DEFAULT_FROM_EMAIL, [], addr_list)
        email.attach_alternative(html_msg, 'text/html')
        email.send(fail_silently=False)
        return render_to_response('invite_done.html',
                                  context_instance=RequestContext(request))
    uri = request.build_absolute_uri("/")
    return render_to_response('invite.html', {"uri": uri}, context_instance=RequestContext(request))
