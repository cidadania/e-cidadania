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

from django.shortcuts import render_to_response, get_object_or_404
from django.utils.safestring import mark_safe
from django.template import RequestContext
from django.utils import translation
from django.core.exceptions import PermissionDenied

from core.spaces.models import Event, Space
from apps.ecidadania.cal.models import EventCalendar
from e_cidadania import settings


def calendar(request, space_url, year, month):

    """
    Returns an localized event calendar with all the Meeting objects.

    :Context: calendar, nextmonth, prevmonth, get_place
    :Returns: Localized HTML Calendar
    """
    space = get_object_or_404(Space, url=space_url)

    if request.user.has_perm('view_space', space):
        # Avoid people writing wrong numbers or any program errors.
        if int(month) not in range(1, 13):
            return render_to_response('cal/error.html',
                context_instance=RequestContext(request))

        place = get_object_or_404(Space, url=space_url)
        events = Event.objects.order_by('event_date').filter(space=place,
            event_date__year=year, event_date__month=month)

        cur_year, cur_month = int(year), int(month)
        next_month = cur_month + 1
        prev_month = cur_month - 1

        cur_lang = translation.get_language()
        cur_locale = translation.to_locale(cur_lang) + '.UTF-8'  # default encoding with django
        cal = EventCalendar(events, settings.FIRST_WEEK_DAY).formatmonth(cur_year, cur_month)

        # This code is quite strange, it worked like a charm, but one day it returned
        # a "too many values to unpack" error, and then just by removing the locale
        # declaration it worked, but the best thing is... it still translates the calendar!
        # For gods sake someone explain me this black magic.

        # cal = EventCalendar(meetings, settings.FIRST_WEEK_DAY, cur_locale).formatmonth(cur_year, cur_month)

        return render_to_response('cal/calendar.html',
                                  {'calendar': mark_safe(cal),
                                   'nextmonth': next_month,
                                   'prevmonth': prev_month,
                                   'get_place': place},
                                   context_instance=RequestContext(request))
    else:
        raise PermissionDenied
