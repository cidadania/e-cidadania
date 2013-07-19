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
