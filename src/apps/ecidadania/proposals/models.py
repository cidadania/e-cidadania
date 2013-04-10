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
Proposal data models are the ones to store the data inside the DB.
"""

import datetime
from django.core import urlresolvers

from django import forms
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from apps.thirdparty.tagging.fields import TagField
from apps.thirdparty.tagging.models import Tag
from core.spaces.models import Space
from apps.ecidadania.debate.models import Debate

CLOSE_REASONS = (
    (1, _('Economically not viable')),
    (2, _('Legally not viable')),
    (3, _('Technically not viable')),
    (4, _('Offtopic'))
)

OPTIONAL_FIELDS = (
    ('tags', _('Tags')),
    ('latitude', _('Latitude')),
    ('longitude', _('Longitude'))
)


class BaseProposalAbstractModel(models.Model):

    """
    Integrated generic relation into the proposal module, which will allow
    the proposal module to be related to any other module in e-cidadania.

    .. versionadded:: 0.1.5b

    :automatically filled fields: contype_type, object_pk

    """

    content_type = models.ForeignKey(ContentType, null=True, blank=True)
    object_pk = models.TextField(_('object ID'), null=True)
    content_object = generic.GenericForeignKey(ct_field="content_type", fk_field="object_pk")

    class Meta:
        abstract = True


class Category(BaseProposalAbstractModel):

    """
    Dummy class for proposal categories. Inherits directly from
    :class:`BaseClass` without adding any fields.
    """
    pass


class ProposalSet(models.Model):

    """
    ProposalSet date model. This will contain a group of proposal
    which will be created after the debate using the debate note after it is
    finished.

    .. addedversion:: 0.1.5b

    :automatically filled fields: space, author, pub_date, debate
    :user filled fields: Name

    """

    name = models.CharField(_('Name'), max_length=200, unique=True,
                            help_text=_('Max: 200 characters'))
    # ptype = models.CharField(_('Ponderation'), choices=PONDERATIONS,
    #     max_length=20, help_text=_('Ponderation types:<br><strong>Users: \
    #     </strong>Users give support votes to the proposal, and that votes \
    #     are added to the final voting.<br><strong>Fixed:</strong>Fixed \
    #     ponderations are stablished by the process managers. It\'s a \
    #     porcentual puntuation. That means that percetange is calculated \
    #     after the voting and added to the final voting.<br><strong>None: \
    #     </strong> No ponderation is applied to the final voting.'))
    space = models.ForeignKey(Space, blank=True, null=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, blank=True, null=True)
    debate = models.ForeignKey(Debate, blank=True, null=True,
        help_text=_('Select the debate associated with this proposal set'))

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('Proposal set')
        verbose_name_plural = _('Proposal sets')
        get_latest_by = 'pub_date'

    @models.permalink
    def get_absolute_url(self):
        return ('view-proposalset', (), {
            'space_url': self.space.url,
            'set_id': self.id
        })


class Proposal(BaseProposalAbstractModel):

    """
    Proposal data model. This will store the user proposal in a similar
    way that Stackoverflow does. Take in mind that this data model is very
    exhaustive because it covers the administrator and the user.

    :automatically filled fields: Space, Author, Pub_date, mod_date.
    :user filled fields: Title, Description, Tags, Latitude, Longitude.
    :admin fields (manual): Code, Closed, Close_reason, Anon_allowed,
                            Refurbished, Budget.
    :admin fields (auto): Closed_by
    :extra permissions: proposal_view

    :const:`CLOSE_REASONS` for :class:Proposal data model is hardcoded with four values, which will fit most of the requirements.
    """
    code = models.CharField(_('Code'), max_length=50, blank=True,
        null=True)
    title = models.CharField(_('Title'), max_length=100, unique=True,
        help_text=_('Max: 200 characters'))
    proposalset = models.ForeignKey(ProposalSet, related_name='proposal_in',
        blank=True, null=True, help_text=_('Proposal set in which the \
        proposal resides'))
    description = models.TextField(_('Description'), max_length=300)
    space = models.ForeignKey(Space, blank=True, null=True)
    author = models.ForeignKey(User, related_name='proposal_authors',
        blank=True, null=True, help_text=_('Change the user that will \
        figure as the author'))
    tags = TagField(help_text=_('Insert here relevant words related with \
        the proposal'))
    latitude = models.DecimalField(_('Latitude'), blank=True, null=True,
        max_digits=17, decimal_places=15, help_text=_('Specify it in decimal'))
    longitude = models.DecimalField(_('Longitude'), blank=True, null=True,
        max_digits=17, decimal_places=15, help_text=_('Specify it in decimal'))
    closed = models.NullBooleanField(default=False, blank=True)
    closed_by = models.ForeignKey(User, blank=True, null=True,
        related_name='proposal_closed_by')
    close_reason = models.SmallIntegerField(choices=CLOSE_REASONS, null=True,
        blank=True)
    merged = models.NullBooleanField(default=False, blank=True, null=True)
    merged_proposals = models.ManyToManyField('self', blank=True, null=True,
        help_text=_("Select proposals from the list"))

    anon_allowed = models.NullBooleanField(default=False, blank=True)
    support_votes = models.ManyToManyField(User, null=True, blank=True,
        verbose_name=_('Support votes from'), related_name='support_votes')
    votes = models.ManyToManyField(User, verbose_name=_('Votes from'),
        null=True, blank=True, related_name='voting_votes')
    refurbished = models.NullBooleanField(default=False, blank=True)
    budget = models.IntegerField(blank=True, null=True)

    pub_date = models.DateTimeField(auto_now_add=True)
    mod_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title

    def set_tags(self, tags):
        Tag.objects.update_tags(self, tags)

    def get_tags(self, tags):
        return Tag.objects.get_for_object(self)

    class Meta:
        verbose_name = _('Proposal')
        verbose_name_plural = _('Proposals')
        get_latest_by = 'pub_date'

    @models.permalink
    def get_absolute_url(self):
        return ('view-proposal', (), {
            'space_url': self.space.url,
            'prop_id': str(self.id)})


class ProposalField(models.Model):

    """
    Proposal Fields data model. This will store details of addition form
    fields which can be optionally added the proposal form which is residing
    in a particular proposal set.

    user filled fields: proposalset, field_name
    const:`OPTIONAL_FIELD` for class:ProposalField is hardcoded with three
    field values, more fields can be added as need.

    """

    proposalset= models.ForeignKey(ProposalSet, help_text=_('Customizing \
        proposal form for a proposal set'), unique=False)
    field_name = models.CharField(max_length=100, choices=OPTIONAL_FIELDS, help_text=_('Additional field that needed to added to the proposal \
        form'))

    def __unicode__(self):
        return self.field_name

    class Meta:
        verbose_name = _('ProposalField')
        verbose_name_plural = _('ProposalFields')
