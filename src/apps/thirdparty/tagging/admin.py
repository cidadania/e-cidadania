from django.contrib import admin
from apps.thirdparty.tagging.models import Tag, TaggedItem
from apps.thirdparty.tagging.forms import TagAdminForm


class TagAdmin(admin.ModelAdmin):
    form = TagAdminForm

admin.site.register(TaggedItem)
admin.site.register(Tag, TagAdmin)
