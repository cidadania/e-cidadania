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

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.auth.models import User, Group


class StaticPage(models.Model):

    """
    Create basic static pages.
    """
    name = models.CharField(_('Page Title'), max_length=100)
    uri = models.CharField(_('URL'), max_length=50)
    content = models.TextField(_('Content'))
    show_footer = models.BooleanField(_('Show in footer'))
    author = models.ForeignKey(User, blank=True, null=True, verbose_name=_('Author'))
    pub_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(_('Last update'), auto_now=True)
    order = models.IntegerField(_('Order'))

    class Meta:
        ordering = ['name']
        verbose_name_plural = _('Static Pages')

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('view-page', (), {
            'slug': self.uri})
