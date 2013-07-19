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

"""
The calendar module calls a version of Python HTML Calendar and adds some
functions to use django objects with it.

The source code is based on the work of Eivind Uggedal <eivind@uggedal.com>
"""

from calendar import LocaleHTMLCalendar
from datetime import date
from itertools import groupby

from django.utils.html import conditional_escape as esc


class EventCalendar(LocaleHTMLCalendar):

    """
    Event calendar is a basic calendar made with HTMLCalendar module and
    its instance LocaleHTMLCalendar for translation.

    :Attributes: LocaleHTMLCalendar
    :Methods: formatday, formatmonth, group_by_day, day_cell
    """
    # This init is needed for multilanguage, see ticket #86

    def __init__(self, events, *args, **kwargs):
        self.events = self.group_by_day(events)
        super(EventCalendar, self).__init__(*args, **kwargs)

#    def __init__(self, events):
#        super(EventCalendar, self).__init__()
#        self.events = self.group_by_day(events)

    def formatday(self, day, weekday):

        """
        Format the day cell with the current events for the day.
        """
        if day != 0:
            cssclass = self.cssclasses[weekday]
            if date.today() == date(self.year, self.month, day):
                cssclass += ' today'
            if day in self.events:
                cssclass += ' filled'
                body = ['<ul>']
                for event in self.events[day]:
                    body.append('<li>')
                    body.append('<a href="%s">' % event.get_absolute_url())
                    body.append(esc(event.title))
                    body.append('</a></li>')
                body.append('<ul>')
                return self.day_cell(cssclass, '%d %s' % (day, ''.join(body)))
            return self.day_cell(cssclass, day)
        return self.day_cell('noday', '&nbsp;')

    def formatmonth(self, year, month):

        """
        Format the current month wuth the events.
        """
        # WTF is this!?
        self.year, self.month = year, month
        return super(EventCalendar, self).formatmonth(self.year, self.month)

    def group_by_day(self, events):

        """
        Group the returned events into their respective dates.
        """
        field = lambda event: event.event_date.day
        return dict(
            [(day, list(items)) for day, items in groupby(events, field)]
        )

    def day_cell(self, cssclass, body):

        """
        Create the day cell.
        """
        return '<td class="%s">%s</td>' % (cssclass, body)
