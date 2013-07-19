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

from django import template
from django.template import Library

from e_cidadania.apps.debate.models import Note, Debate
from django.shortcuts import get_object_or_404

register = Library()


class NotesNode(template.Node):
    """
    """
    def __init__(self, format_string):
        self.format_string = format_string
        self.debate = get_object_or_404(Debate, pk=format_string)
        self.debate_matrix = len(self.debate.xvalues.split(',')) * \
                             len(self.debate.yvalues.split(','))

    def render(self, context):
        i = 1
        while i < self.debate_matrix:
            get_sortable = "sortable-debate%s" % i
            try:
                note = Note.objects.all().filter(parent=get_sortable, debate=self.format_string)
                return "<td id='%s' class='connectedSortable'>\
                            <div id='%s' class='note'>\
                                <a href='javascript:getClickedNote()' id='deletenote' class='hidden'></a>\
                                <textarea>%s</textarea>\
                            </div>\
                        </td>" % (get_sortable, note.noteid, note.message)
                i += 1
            except:
                return "<td id='%s' class='connectedSortable'></td>" % (get_sortable)
                i += 1


@register.tag
def get_debate_notes(parser, token):
    """
    Generate the notes for the debate.
    """
    try:
        tag_name, format_string = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r requires a single argument." % token.contents.split()[0])
#    The current style of template tags does not consider the quotes an obligation.
#    if not (format_string[0] == format_string[-1] and format_string[0] in ('"', "'")):
#        raise template.TemplateSyntaxError("%r tag's argument should be in quotes" % tag_name)
    if not format_string.isdigit():
        raise template.TemplateSyntaxError("%r is not a valid debate id." % format_string)
    return NotesNode(format_string)
