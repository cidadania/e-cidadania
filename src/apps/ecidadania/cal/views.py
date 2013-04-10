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

from django.shortcuts import render_to_response, get_object_or_404
from django.utils.safestring import mark_safe
from django.template import RequestContext
from django.utils import translation

from core.spaces.models import Event, Space
from apps.ecidadania.cal.models import EventCalendar
from e_cidadania import settings


def calendar(request, space_url, year, month):

    """
    Returns an localized event calendar with all the Meeting objects.

    :Context: calendar, nextmonth, prevmonth, get_place
    :Returns: Localized HTML Calendar
    """
    # Avoid people writing wrong numbers or any program errors.
    if int(month) not in range(1, 13):
        return render_to_response('cal/error.html',
                                  context_instance=RequestContext(request))

    place = get_object_or_404(Space, url=space_url)
    events = Event.objects.order_by('event_date') \
                              .filter(space=place,
                                      event_date__year=year,
                                      event_date__month=month)

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
