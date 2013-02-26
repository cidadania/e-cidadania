from django.conf import settings

# Enable the sidebar custom menu or just render the regular tree? Default: False
if hasattr(settings, 'CUSTOM_MENU'):
    CUSTOM_MENU = settings.CUSTOM_MENU
else:
    CUSTOM_MENU = False

# If you use a custom menu what apps does it display. Default: Same as APP_MENU
if hasattr(settings, 'SIDEBAR_APP_MENU'):
    SIDEBAR_APP_MENU = settings.SIDEBAR_APP_MENU
else:
    SIDEBAR_APP_MENU = [
            {"name": "Users and Settings",
             "items": ["auth", "prismriver", "sites"],
             "icon": "users.png",
             },
    ]

#Display Last actions on the sidebar? Default:True
if hasattr(settings, 'SIDEBAR_LAST_ACTIONS'):
    SIDEBAR_LAST_ACTIONS = settings.SIDEBAR_LAST_ACTIONS
else:
    SIDEBAR_LAST_ACTIONS = True

# If you use the default menu which labels and pictures you want for the sidebar
if hasattr(settings, 'DEFAULT_LABELS'):
    DEFAULT_LABELS = settings.DEFAULT_LABELS
else:
    DEFAULT_LABELS = {"auth/": ["Users and Groups", "users.png", "users_big.png",
                                "Manage the application users or groups permissions"],
                      "sites/": ["Site management", "web.png", "web_big.png", "Manages the sites application"]}