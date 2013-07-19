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
        permissions = (
            ('view', 'Can view the page'),
        )

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('view-page', (), {
            'slug': self.uri})
