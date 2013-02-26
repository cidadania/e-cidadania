from django.db import models
from django.utils.translation import ugettext_lazy as _
from prismriver.dashboard.settings import HOMESCREEN_PLUGIN_CHOICES
from django.contrib.auth.models import User

class HomeScreen(models.Model):
    user = models.ForeignKey(User, unique=True)


class Plugin(models.Model):
    home_screen = models.ForeignKey(HomeScreen)
    position = models.IntegerField(verbose_name=_("Plugin position"))
    class_name = models.CharField(max_length=128,
                                  choices=HOMESCREEN_PLUGIN_CHOICES,
                                  verbose_name=_("Plugin Classname"))

    class Meta:
        verbose_name = _("Plugin")
        verbose_name_plural = _("Plugins")

