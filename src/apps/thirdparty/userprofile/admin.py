from django.contrib import admin
from apps.thirdparty.userprofile.models import EmailValidation, Avatar


class EmailValidationAdmin(admin.ModelAdmin):
    list_display = ('__unicode__',)
    search_fields = ('user__username', 'user__first_name')

admin.site.register(Avatar)
admin.site.register(EmailValidation, EmailValidationAdmin)
