from django.conf import settings

# The app menu (this is used by the App menu site plugin:
# Default: Joins Prismriver auth and sites in a menu named Users and settings
if hasattr(settings, 'APP_MENU'):
    APP_MENU = settings.APP_MENU
else:
    APP_MENU = [
            {"name": "Users and Settings",
             "items": ["auth", "prismriver", "sites"],
             "icon": "users.png",
             "big_icon": "users_big.png",
             "description": "Manage everything about the users here",
             },
              ]

#Plugin choices
if hasattr(settings, 'HOMESCREEN_PLUGIN_CHOICES'):
    HOMESCREEN_PLUGIN_CHOICES = settings.HOMESCREEN_PLUGIN_CHOICES
else:
    HOMESCREEN_PLUGIN_CHOICES = (('prismriver.dashboard.plugins.dashplugins.AppList', 'App list'),
        )