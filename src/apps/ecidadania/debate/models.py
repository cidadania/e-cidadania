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
This file contains all the data models for the debate module.
"""
import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

from taggit.managers import TaggableManager

from core.spaces.models import Space


class Debate(models.Model):

    """
    Debate object. In every space there can be unlimited debates, each one of
    them holds all the related notes. Debates are filtered by space. Start/End
    dates are for letting users use the debate or not.

    .. versionadded:: 0.1b
    """
    title = models.CharField(_('Title'), max_length=200, unique=True)
    description = models.TextField(_('Description'), blank=True, null=True)
    theme = models.CharField(_('Theme'), blank=True, null=True, max_length=100)

    space = models.ForeignKey(Space, blank=True, null=True)
    date = models.DateTimeField(_('Date created'), auto_now_add=True)
    date_mod = models.DateTimeField(_('Last update'), auto_now=True)
    author = models.ForeignKey(User, blank=True, null=True)
    start_date = models.DateField(_('Start date'))
    end_date = models.DateField(_('End date'))
    private = models.BooleanField(_('Private'), help_text=_('Set the debate as private so only the accepted users can participate in it.'))

    class Meta:
        permissions = (
            ('view_debate', 'Can view the debate'),
            ('admin_debate', 'Can administrate the debate'),
            ('mod_debate', 'Can moderate the debate'),
        )

    def __unicode__(self):
        return self.title

    def is_active(self):
        if datetime.date.today() >= self.end_date or datetime.date.today() <= self.start_date:
            return False
        else:
            return True

    @models.permalink
    def get_absolute_url(self):
        return ('view-debate', (), {
            'space_url': self.space.url,
            'debate_id': str(self.id)})

    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError('The start date can not be after the end date.')


class Column(models.Model):
    """
    Debate column object. The debate table is done mixing columns and rows. The column
    object is linked to the debate, but with no preferable order.

    .. versionadded:: 0.1b
    """
    criteria = models.CharField(_('Criteria'), max_length=100, blank=True, null=True)
    debate = models.ForeignKey(Debate, blank=True, null=True)

    def __unicode__(self):
        return self.criteria


class Row(models.Model):
    """
    Row object for the debate system.  The row object works exactly like the
    column. It's associated to the debate in no preferred order.

    .. versionadded:: 0.1b
    """
    criteria = models.CharField(_('Criteria'), max_length=100, blank=True, null=True)
    debate = models.ForeignKey(Debate, blank=True, null=True)

    def __unicode__(self):
        return self.criteria


class Note(models.Model):

    """
    The most important object in every debate, the message. It has a coordinates
    value to determine the position of the note in its debate.

    .. versionadded:: 0.1b
    """
    column = models.ForeignKey(Column, null=True, blank=True)
    row = models.ForeignKey(Row, null=True, blank=True)
    debate = models.ForeignKey(Debate, null=True, blank=True)
    title = models.CharField(_('Title'), max_length=60, blank=True, null=True)
    message = models.TextField(_('Message'), max_length=100, null=True, blank=True)

    date = models.DateTimeField(_('Date created'), auto_now_add=True)
    author = models.ForeignKey(User, null=True, blank=True, related_name="note_author")
    last_mod_author = models.ForeignKey(User, null=True, blank=True, related_name="update_author")
    last_mod = models.DateTimeField(_('Last modification time'), auto_now=True)

    def __unicode__(self):
        return self.message

    class Meta:
        permissions = (
            ('move', 'Can move note'),
        )
