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
This file contains all the forms for the debate modules.
"""

from django.forms import ModelForm, Textarea, TextInput
from django.forms.models import modelformset_factory

from apps.ecidadania.debate.models import Debate, Note, Row, Column


class DebateForm(ModelForm):

    """
    Returns an empty form for creating a new Debate.

    :rtype: HTML Form

    .. versionadded:: 0.1b
    """
    class Meta:
        model = Debate
        widgets = {
            'title': TextInput(attrs={'class': 'medium'}),
        }

RowForm = modelformset_factory(Row, exclude=('debate'))
ColumnForm = modelformset_factory(Column, exclude=('debate'))


class NoteForm(ModelForm):

    """
    Returns an HTML Form to create or edit a new 'note' or 'proposal' like it's
    called on the sociologists argot.

    :rtype: HTML Form

    .. versionadded:: 0.1b
    """
    class Meta:
        model = Note


class UpdateNoteForm(ModelForm):

    """
    Returns a more simple version of the NoteForm for the AJAX interaction,
    preventing modification of significative fields non relevant to AJAX.

    :rtype: HTML Form
    .. versionadded:: 0.1b
    """
    class Meta:
        model = Note
        exclude = ('debate', 'author', 'row', 'column', 'date')


class UpdateNotePosition(ModelForm):

    """
    This is a partial form to save only the position updates of the notes in the
    debates. This form excludes all the fields except Column and Row just for
    security, this wau the original data of the note cannot be modified. Moving
    notes does not count as modification, so we also exclude last modification data.

    :rtype: HTML Form
    .. versionadded:: 0.1.5
    """
    class Meta:
        model = Note
        exclude = ('author', 'debate', 'last_mod', 'last_mod_author', 'date',
            'message', 'title')
