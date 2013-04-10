from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response
from django.contrib.admin.views.decorators import staff_member_required

from django import template
from django.core.urlresolvers import reverse
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.text import capfirst
from core.prismriver.settings import CUSTOM_MENU, DEFAULT_LABELS
from core.prismriver.dashboard.models import Plugin


def separate_class_path(class_path):
    path = class_path.split(".")
    class_name = path.pop()
    class_path = ".".join([i for i in path])
    return str(class_path), str(class_name)


@staff_member_required
def dashboard(request):
    rendered_plugins = []
    plugins = Plugin.objects.filter(home_screen__user__username=request.user.username).order_by("position")
    for p in plugins:
        class_path, class_name = separate_class_path(p.class_name)
        plugin = getattr(__import__(class_path, globals(),
                                    locals(), [class_name]), class_name)()
        rendered_plugins.append(plugin.render(request))
    context = {
        'title': _('Site administration'),
        'plugins': rendered_plugins,
    }
    context.update({})
    context_instance = template.RequestContext(request)
    return render_to_response('admin/dashboard.html', context,
                              context_instance=context_instance)
