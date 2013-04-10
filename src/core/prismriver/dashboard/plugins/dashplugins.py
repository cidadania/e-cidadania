from django.core.urlresolvers import reverse
from django.template.context import Context
from django.template.loader import get_template
from core.prismriver.dashboard.plugins import pluginbase
from core.prismriver.settings import CUSTOM_MENU
from core.prismriver.dashboard.settings import APP_MENU
from core.prismriver.views import load_apps, load_custom_models
from copy import deepcopy


class AppList(pluginbase.DashboardPlugin):
    def get_custom_menu(self, request):
        apps = deepcopy(APP_MENU)
        for app in apps:
            app["models"], app["enabled"] = load_custom_models(request, app["items"])
        c = Context({"apps": apps})
        t = get_template('plugins/app_menu.html')
        return t.render(c)

    def get_menu(self, request):
        current_url = request.path.replace(reverse('admin:index'), "").lower()
        c = Context({"apps": load_apps(request)})
        t = get_template('plugins/app_menu.html')
        return t.render(c)

    def render(self, request):
        if CUSTOM_MENU:
            return self.get_custom_menu(request)
        else:
            return self.get_menu(request)
