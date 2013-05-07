# -*- coding: utf-8 -*-
#
# Copyright (c) 2010-2013 Cidadania S. Coop. Galega
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


from django.contrib import messages
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from core.spaces.models import Space
from e_cidadania import settings


def index_view(request):

    """
    Main view for the index page. It's separated from the urls.py file
    because using direct_to_template in urls.py doesn't refresh the content
    (it's loaded only once).
    """
    space_list = Space.objects.filter(public=True)

    extra_context = {
        'spaces': space_list,
        'version': settings.__version__,
        'status': settings.__status__,
        'debug_mode': settings.DEBUG,
        #'cache_timeout': 500,
    }

    if request.user.is_anonymous():
        messages.info(request, _("Hi! It seems that it's your first time \
        here. Maybe you want to <a href=\"/accounts/register\">register</a> \
        or <a href=\"/accounts/login/\">login</a> if you have an account."))

        return render_to_response('site_index.html', extra_context,
                              context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect(reverse('profile_overview'))
