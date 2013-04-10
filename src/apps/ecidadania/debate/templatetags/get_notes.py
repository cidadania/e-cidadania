# -*- coding: utf-8 -*-
#
# Copyright (c) 2010 Cidadanía Coop.
# Written by: Oscar Carballal Prego <info@oscarcp.com>
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
