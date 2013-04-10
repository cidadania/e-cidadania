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

from datetime import datetime

from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from core.spaces.file_validation import ContentTypeRestrictedFileField
from fields import StdImageField
from allowed_types import ALLOWED_CONTENT_TYPES


class Space(models.Model):

    """
    Spaces model. This model stores a "space" or "place" also known as a
    participative process in reality. Every place has a minimum set of
    settings for customization.

    There are three main permission roles in every space: administrator
    (admins), moderators (mods) and regular users (users).
    """
    name = models.CharField(_('Name'), max_length=250, unique=True,
        help_text=_('Max: 250 characters'))
    url = models.CharField(_('URL'), max_length=100, unique=True,
        validators=[RegexValidator(regex='^[a-z0-9_]+$',
        message='Invalid characters in the space URL.')],
        help_text=_('Valid characters are lowercase, digits and \
                     underscore. This will be the accesible URL'))
    description = models.TextField(_('Description'),
        default=_('Write here your description.'))
    date = models.DateTimeField(_('Date of creation'), auto_now_add=True)
    author = models.ForeignKey(User, blank=True, null=True,
        verbose_name=_('Space creator'), help_text=_('Select a user that \
        will be marked as creator of the space'))
    logo = StdImageField(upload_to='spaces/logos', size=(100, 75, False),
        help_text = _('Valid extensions are jpg, jpeg, png and gif'))
    banner = StdImageField(upload_to='spaces/banners', size=(500, 75, False),
        help_text = _('Valid extensions are jpg, jpeg, png and gif'))
    public = models.BooleanField(_('Public space'), help_text=_("This will \
        make the space visible to everyone, but registration will be \
        necessary to participate."))
    # theme = models.CharField(_('Theme'), m)
    admins = models.ManyToManyField(User, related_name="space_admins", verbose_name=_('Administrators'), help_text=_('Please select the \
        users that will be administrators of this space'), blank=True,
        null=True)
    mods = models.ManyToManyField(User, related_name="space_mods",
        verbose_name=_('Moderators'), help_text=_('Please select the users \
        that will be moderators of this space.'), blank=True, null=True)
    users = models.ManyToManyField(User, related_name="space_users", verbose_name=_('Users'), help_text=_('Please select the users that \
        can participate on this space'), blank=True, null=True)

# Modules
    mod_debate = models.BooleanField(_('Debate'))
    mod_proposals = models.BooleanField(_('Proposals'))
    mod_news = models.BooleanField(_('News'))
    mod_cal = models.BooleanField(_('Calendar'))
    mod_docs = models.BooleanField(_('Documents'))
    mod_voting = models.BooleanField(_('Voting'))

    class Meta:
        ordering = ['name']
        verbose_name = _('Space')
        verbose_name_plural = _('Spaces')
        get_latest_by = 'date'
        permissions = (
            ('view', 'Can view this space.'),
        )

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('space-index', (), {
                'space_url': self.url})


class Entity(models.Model):

    """
    This model stores the name of the entities responsible for the creation
    of the space or supporting it.
    """
    name = models.CharField(_('Name'), max_length=100, unique=True)
    website = models.CharField(_('Website'), max_length=100, null=True,
        blank=True)
    logo = models.ImageField(upload_to='spaces/logos', verbose_name=_('Logo'),
        blank=True, null=True)
    space = models.ForeignKey(Space, blank=True, null=True)

    class Meta:
        ordering = ['name']
        verbose_name = _('Entity')
        verbose_name_plural = _('Entities')

    def __unicode__(self):
        return self.name


class Document(models.Model):

    """
    This models stores documents for the space, like a document repository,
    There is no restriction in what a user can upload to the space.

    :methods: get_file_ext, get_file_size
    """
    title = models.CharField(_('Document title'), max_length=100,
        help_text=_('Max: 100 characters'))
    space = models.ForeignKey(Space, blank=True, null=True,
        help_text=_('Change the space to whom belongs this document'))
    docfile = ContentTypeRestrictedFileField(_('File'),
        upload_to='spaces/documents/%Y/%m/%d',
        content_types=ALLOWED_CONTENT_TYPES,
        max_upload_size=26214400,
        help_text=_('Permitted file types: DOC, DOCX, PPT, ODT, ODF, ODP, \
            PDF, RST, TXT.'))
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, verbose_name=_('Author'), blank=True,
        null=True, help_text=_('Change the user that will figure as the \
        author'))

    def get_file_ext(self):
        filename = self.docfile.name
        extension = filename.split('.')
        return extension[1].upper()

    def get_file_size(self):
        if self.docfile.size < 1023:
            return str(self.docfile.size) + " Bytes"
        elif self.docfile.size >= 1024 and self.docfile.size <= 1048575:
            return str(round(self.docfile.size / 1024.0, 2)) + " KB"
        elif self.docfile.size >= 1048576:
            return str(round(self.docfile.size / 1024000.0, 2)) + " MB"

    class Meta:
        ordering = ['pub_date']
        verbose_name = _('Document')
        verbose_name_plural = _('Documents')
        get_latest_by = 'pub_date'

    # There is no 'view-document' view, so I'll leave the get_absolute_url
    # method without permalink. Remember that the document files are accesed
    # through the url() method in templates.
    def get_absolute_url(self):
        return '/spaces/%s/docs/%s' % (self.space.url, self.id)


class Event(models.Model):

    """
    Meeting data model. Every space (process) has N meetings. This will
    keep record of the assistants, meeting name, etc.
    """
    title = models.CharField(_('Event name'), max_length=250,
        help_text="Max: 250 characters")
    space = models.ForeignKey(Space, blank=True, null=True)
    user = models.ManyToManyField(User, verbose_name=_('Users'),
        help_text=_('List of the users that will assist or assisted to the \
        event.'))
    pub_date = models.DateTimeField(auto_now_add=True)
    event_author = models.ForeignKey(User, verbose_name=_('Created by'),
        blank=True, null=True, related_name='meeting_author',
        help_text=_('Select the user that will be designated as author.'))
    event_date = models.DateField(verbose_name=_('Event date'),
        help_text=_('Select the date where the event is celebrated.'))
    description = models.TextField(_('Description'), blank=True, null=True)
    location = models.TextField(_('Location'), blank=True, null=True)
    latitude = models.DecimalField(_('Latitude'), blank=True, null=True,
        max_digits=17, decimal_places=15, help_text=_('Specify it in decimal'))
    longitude = models.DecimalField(_('Longitude'), blank=True, null=True,
        max_digits=17, decimal_places=15, help_text=_('Specify it in decimal'))

    def is_due(self):
        if self.pub_date < datetime.now():
            return True
        else:
            return False

    class Meta:
        ordering = ['event_date']
        verbose_name = _('Event')
        verbose_name_plural = _('Events')
        get_latest_by = 'event_date'
        permissions = (
            ('view', 'Can view this event'),
        )

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('view-event', (), {
            'space_url': self.space.url,
            'event_id': str(self.id)})


class Intent(models.Model):

    """
    Intent data model. Intent stores the reference of a user-token when a user
    asks entering in a restricted space.

    .. versionadded: 0.1.5
    """
    user = models.ForeignKey(User)
    space = models.ForeignKey(Space)
    token = models.CharField(max_length=32)
    requested_on = models.DateTimeField(auto_now_add=True)

    def get_approve_url(self):
        site = Site.objects.all()[0]
        return "http://%s%sintent/approve/%s" % (site.domain, self.space.get_absolute_url(), self.token)
