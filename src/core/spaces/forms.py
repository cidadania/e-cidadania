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
This module contains all the space related forms, including the forms for
documents, meetings and entities. Most of the forms are directly generated
from the data models.
"""

from django.forms import ModelForm, ValidationError, Select
from django.forms.models import modelformset_factory

from core.spaces.models import Space, Document, Event, Entity


class SpaceForm(ModelForm):

    """
    Returns a form to create or edit a space. SpaceForm inherits all the fields
    from the :class:`Space` data model.

    :rtype: HTML Form

    .. versionadded:: 0.1
    """
    class Meta:
        model = Space

    def clean_logo(self):
        valid_image_extensions = ['jpg', 'jpeg', 'png', 'gif']
        logo_file = self.cleaned_data['logo']
        for extension in valid_image_extensions:
            if logo_file.name.endswith(''.join(['.', extension])):
                return logo_file

        raise ValidationError("Invalid file extension")

    def clean_banner(self):
        valid_image_extensions = ['jpg', 'jpeg', 'png', 'gif']
        banner_file = self.cleaned_data['banner']
        for extension in valid_image_extensions:
            if banner_file.name.endswith(''.join(['.', extension])):
                return banner_file

        raise ValidationError("Invalid file extension")

# Create a formset for entities. This formset can be attached to any other form
# but will be usually attached to SpaceForm
EntityFormSet = modelformset_factory(Entity, extra=3)


class DocForm(ModelForm):

    """
    Returns a form to create or edit a space related document, based on the
    spaces.Document data model.

    :rtype: HTML Form

    .. versionadded:: 0.1
    """
    class Meta:
        model = Document


class RoleForm(ModelForm):

    """
    Returns a form to edit the administrators, moderators and users of the space.
    This is the way that e-cidadania uses to filter content and access.

    :rtype: HTML Form

    .. versionadded:: 0.1.5
    """
    class Meta:
        model = Space
        exclude = ('name', 'url', 'date', 'description', 'date', 'logo', 'banner',
            'author', 'mod_debate', 'mod_proposals', 'mod_news', 'mod_cal',
            'mod_docs', 'mod_voting', 'public')


class EventForm(ModelForm):

    """
    Returns a form to create or edit a space related meeting, based on the
    spaces.Meeting data model.

    :rtype: HTML Form

    .. versionadded:: 0.1
    """
    class Meta:
        model = Event
