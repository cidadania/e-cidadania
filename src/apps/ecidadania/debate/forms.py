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
