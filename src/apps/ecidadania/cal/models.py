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
