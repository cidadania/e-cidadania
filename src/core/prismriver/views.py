from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response
from django.contrib.admin.views.decorators import staff_member_required

from django import template
from django.core.urlresolvers import reverse
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.text import capfirst
from core.prismriver.settings import CUSTOM_MENU, DEFAULT_LABELS


def load_apps(request):
    current_url = request.path.replace(reverse('admin:index'), "")
    app_dict = {}
    enabled = False
    for model, model_admin in admin.site._registry.items():
        app_label = model._meta.app_label
        has_module_perms = request.user.has_module_perms(app_label)
        if has_module_perms:
            perms = model_admin.get_model_perms(request)
            if True in perms.values():
                if '%s/%s/' % (app_label, model.__name__.lower()) in current_url.lower():
                    enabled = True
                else:
                    enabled = False
                model_dict = {
                    'name': capfirst(model._meta.verbose_name_plural),
                    'admin_url': mark_safe('%s/%s/' % (app_label, model.__name__.lower())),
                    'perms': perms,
                }
                if app_label in app_dict:
                    app_dict[app_label]['models'].append(model_dict)
                    if enabled:
                        app_dict[app_label]["enabled"] = enabled
                else:
                    app_dict[app_label] = {
                        'name': app_label.title(),
                        'app_url': app_label + '/',
                        'has_module_perms': has_module_perms,
                        'models': [model_dict],
                        'icon': 'default.png',
                        'big_icon': "default_big.png",
                        'description': _("Default application description"),
                        'enabled': enabled,
                    }
                    if app_dict[app_label]["app_url"] in DEFAULT_LABELS.keys():
                        current_app = DEFAULT_LABELS[app_dict[app_label]["app_url"]]
                        app_dict[app_label]["name"] = current_app[0]
                        app_dict[app_label]["icon"] = current_app[1]
                        app_dict[app_label]["big_icon"] = current_app[2]
                        app_dict[app_label]["description"] = current_app[3]
    app_list = app_dict.values()
    app_list.sort(key=lambda x: x['name'])
    return app_list


def load_custom_models(request, model_paths):
    current_url = request.path.replace(reverse('admin:index'), "")
    enabled = False
    model_list = []
    for model, model_admin in admin.site._registry.items():
        app_label = model._meta.app_label
        has_module_perms = request.user.has_module_perms(app_label)
        if has_module_perms:
            perms = model_admin.get_model_perms(request)
            if True in perms.values():
                current_path = ""
                for model_path in model_paths:
                    current_path = '%s/%s/' % (app_label, model.__name__.lower())
                    if current_url in current_path:
                        enabled = True
                    if model_path in current_path:
                        model_list.append({
                            'name': capfirst(model._meta.verbose_name_plural),
                            'admin_url': mark_safe('%s/%s/' % (app_label, model.__name__.lower())),
                            'perms': perms,
                        })
    return model_list, enabled
