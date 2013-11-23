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

from django.forms import ModelForm
from django.forms.models import modelformset_factory

from apps.ecidadania.voting.models import *
from apps.ecidadania.proposals.models import Proposal, ProposalSet


class PollForm(ModelForm):
        """
        """
        class Meta:
            model = Poll

# Create a formset for choices. This formset can be attached to any other form
# but will be usually attached to PollForm

ChoiceFormSet = modelformset_factory(Choice, exclude=('poll',), extra=5)


class VotingForm(ModelForm):

    """
    """
    class Meta:
        model = Voting

    # This override of the init method allows us to filter the list of
    # elements in proposalsets and proposals
    def __init__(self, current_space, **kwargs):
        super(VotingForm, self).__init__(**kwargs)
        self.fields['proposalsets'].queryset = ProposalSet.objects.filter(
            space=current_space)
        self.fields['proposals'].queryset = Proposal.objects.filter(
            space=current_space)


class VoteForm(ModelForm):

    """
    """
    class Meta:
        model = ConfirmVote
