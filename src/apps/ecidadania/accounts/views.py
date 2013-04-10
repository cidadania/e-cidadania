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

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User

from apps.ecidadania.accounts.models import UserProfile, Phone

# This views are no longer required since they were replaced by userprofile


@login_required
def view_profile(request):

    """
    Return the profile of the current logged user.

    userdata: This variable gets the django basic user profile from
              the current logged in user.
    userprofile: Gets all the variables stored by the model UserProfile
                 using the method get_profile() since it's bound to the
                 user profile in the settings file.

    Template tags
    -------------
    user: returns any of the data stored by the django user profile.
    profile: returns any of the data stored by the UserProfile model.
    """
    userdata = get_object_or_404(User, pk=request.user.id)
    userprofile = User.get_profile(userdata)

    return render_to_response('accounts/profile.html',
                             {'user': userdata, 'profile': userprofile})
