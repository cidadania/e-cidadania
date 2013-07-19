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

from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail, send_mass_mail
from django.template import RequestContext

from e_cidadania import settings
from apps.ecidadania.accounts.models import UserProfile


class ProfileAdmin(admin.ModelAdmin):

    """
    This is a minimal view for Django administration interface. It shows the
    user and the website.
    """
    list_display = ('user', 'firstname', 'surname', 'country', 'website')
    actions = ['mass_mail']

    def mass_mail(self, request, queryset):
        """
        This function exports the selected ovjects to a new view to manipulate
        them properly.
        """
        # selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        # ct = ContentType.objects.get_for_model(queryset.model)
        if 'sendmail' in request.POST:
            for obj in queryset:
                get_user = get_object_or_404(User, id=obj.id)
                send_mail(request.POST['massmail_subject'], request.POST['message'], settings.DEFAULT_FROM_EMAIL, [get_user.email])
            return HttpResponseRedirect(request.get_full_path())

        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        ct = ContentType.objects.get_for_model(queryset.model)
        return render_to_response('mail/massmail.html', {'people': selected},
                                context_instance=RequestContext(request))
    mass_mail.short_description = 'Send a global mail to the selected users'

admin.site.register(UserProfile, ProfileAdmin)
