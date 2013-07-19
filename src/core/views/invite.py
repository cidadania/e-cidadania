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

from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.shortcuts import render_to_response
from django.template import RequestContext, loader, Context
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _

from e_cidadania import settings


@login_required
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
