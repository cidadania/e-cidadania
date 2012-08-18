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

from django.forms import ModelForm
from django.forms.models import modelformset_factory
from apps.ecidadania.voting.models import *


class PollForm(ModelForm):
        """
        """
        class Meta:
            model = Poll

# Create a formset for choices. This formset can be attached to any other form
# but will be usually attached to PollForm

ChoiceFormSet = modelformset_factory(Choice, exclude=('poll'), extra=5)

class VotingForm(ModelForm):
        """
        """
        class Meta:
            model = Voting
