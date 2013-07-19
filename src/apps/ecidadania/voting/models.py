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
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from apps.thirdparty.tagging.fields import TagField
from apps.thirdparty.tagging.models import Tag
from core.spaces.models import Space
from apps.ecidadania.proposals.models import *


PONDERATIONS = (
    ('users', _('Users')),
    ('fixed', _('Fixed')),
    ('none', _('No ponderation'))
)


class Poll(models.Model):

    """
    Data model for Polls. It stores the question and some data like the space
    and dates. The most important field is "participants". It allows us to
    limit the times a user can vote in a Poll, using it with the vote field in
    Choices model.

    .. versionadded:: 0.1.5
    """

    question = models.CharField(_('Question'), max_length=200,
        help_text=_('Max: 200 characters'))
    pub_date = models.DateTimeField(_('Date'), auto_now_add=True)
    poll_lastup = models.DateTimeField(_('Last update'), auto_now=True)
    author = models.ForeignKey(User, verbose_name=_('Author'), blank=True,
        null=True, help_text=_('Change the user that will figure as the \
        author'), related_name='poll-author')
    participants = models.ManyToManyField(User, blank=True, null=True)
    space = models.ForeignKey(Space, verbose_name=_('Publish in'), blank=True,
        null=True, help_text=_('If you want to post to the index leave this \
        blank'))
    poll_tags = TagField(help_text=_('Insert here relevant words related with \
        the poll'))
    start_date = models.DateField(_('Start date'))
    end_date = models.DateField(_('End date'))

    class Meta:
        permissions = (
            ('view', 'Can view the poll'),
        )

    def __unicode__(self):
        return self.question

    def set_tags(self, tags):
        Tag.objects.update_tags(self, tags)

    def get_tags(self, tags):
        return Tag.objects.get_for_object(self)

    @models.permalink
    def get_absolute_url(self):
        if self.space is not None:
            return ('view-polls', (), {
                'space_url': self.space.url,
                'poll_id': str(self.id)})
        else:
            return ('view-polls', (), {
                'poll_id': str(self.id)})

    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError('The start date can not be after the end date.')


class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice_text = models.CharField(_('Choice'), max_length=200, blank=True, null=True, help_text=_('Enter choice to be voted upon'))
    # votes = models.IntegerField(blank=True, null=True, default='0')
    votes = models.ManyToManyField(User, blank=True, null=True)

    @models.permalink
    def get_absolute_url(self):
        if self.space is not None:
            return ('view-polls', (), {
                'space_url': self.space.url,
                'poll_id': str(self.id)})
        else:
            return ('view-polls', (), {
                'poll_id': str(self.id)})


class Voting(models.Model):
    title = models.CharField(_('Title'), max_length=200, unique=True)
    description = models.TextField(_('Description'), blank=True, null=True)

    space = models.ForeignKey(Space, blank=True, null=True)
    date = models.DateTimeField(_('Date created'), auto_now_add=True)
    date_mod = models.DateTimeField(_('Last update'), auto_now=True)
    author = models.ForeignKey(User, blank=True, null=True)
    start_date = models.DateField(_('Start date'), blank=True, null=True)
    end_date = models.DateField(_('End date'), blank=True, null=True)
    ponderation = models.CharField(_('Ponderation'), max_length=3, null=True,
        blank=True, choices=PONDERATIONS)
    proposalsets = models.ManyToManyField(ProposalSet, blank=True, null=True)

    proposals = models.ManyToManyField(Proposal, blank=True, null=True, limit_choices_to={'proposalset__isnull': True})
    max_votes = models.IntegerField(_('Maximum votes per person'), blank=True,
        null=True)

    class Meta:
        permissions = (
            ('view', 'Can view the voting'),
        )

    @models.permalink
    def get_absolute_url(self):
        if self.space is not None:
            return ('view-votings', (), {
                'space_url': self.space.url,
                'voting_id': str(self.id)})
        else:
            return ('view-votings', (), {
                'voting_id': str(self.id)})

    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError('The start date can not be after the end date.')


class ConfirmVote(models.Model):

    """
    Intent data model. Intent stores the reference of a user-token when a user
    asks entering in a restricted space.

    .. versionadded: 0.1.5
    """
    user = models.ForeignKey(User, blank=True, null=True)
    proposal = models.ForeignKey(Proposal, blank=True, null=True)
    token = models.CharField(max_length=32, blank=True, null=True)
    requested_on = models.DateTimeField(auto_now_add=True)

    def get_approve_url(self):
        site = Site.objects.all()[0]
        return "http://%s%svote/approve/%s" % (site.domain, self.proposal.get_absolute_url(), self.token)
