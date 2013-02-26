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
        #selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        # ct = ContentType.objects.get_for_model(queryset.model)
        if 'sendmail' in request.POST:
            for obj in queryset:
                get_user = get_object_or_404(User, id=obj.id)
                send_mail(request.POST['massmail_subject'], request.POST['message'], settings.DEFAULT_FROM_EMAIL, [get_user.email])
            return HttpResponseRedirect(request.get_full_path())
        
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        ct = ContentType.objects.get_for_model(queryset.model)
        return render_to_response('mail/massmail.html', { 'people': selected },
                                context_instance=RequestContext(request))
    mass_mail.short_description = 'Send a global mail to the selected users'
    
admin.site.register(UserProfile, ProfileAdmin)
