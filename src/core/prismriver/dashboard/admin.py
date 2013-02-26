from django.contrib import admin
from prismriver.dashboard.models import HomeScreen, Plugin

class PluginInline(admin.TabularInline):
    extra = 0
    model = Plugin


class HomeScreenAdmin(admin.ModelAdmin):
    list_display = ('user',)
    inlines = (PluginInline,)


admin.site.register(HomeScreen, HomeScreenAdmin)