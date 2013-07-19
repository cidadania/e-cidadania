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

from urlparse import urljoin

from django import template
from django.conf import settings
from django.template import Context, Template
from django.template.defaultfilters import stringfilter
from django.template.loader import get_template, render_to_string

register = template.Library()


@register.simple_tag
def wysiwyg_editor(field_id, editor_name=None, config=None):
    if not editor_name:
        editor_name = "%s_editor" % field_id

    ctx = {
        'field_id': field_id,
        'editor_name': editor_name,
        'config': config
    }

    return render_to_string(
        "../templates/wysihtml5_instance.html",
        ctx
    )
