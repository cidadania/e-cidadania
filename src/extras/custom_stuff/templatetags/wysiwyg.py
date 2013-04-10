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
