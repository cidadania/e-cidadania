from django.conf import settings

if hasattr(settings, "I18N_URLS") and settings.I18N_URLS:
    try:
        module = __import__("apps.thirdparty.userprofile.urls.%s" % (settings.LANGUAGE_CODE),
                            {}, {}, "urlpatterns")
        globals().update({"urlpatterns": module.__dict__["urlpatterns"]})
    except:
        module = __import__("apps.thirdparty.userprofile.urls.en", {}, {}, "urlpatterns")
        globals().update({"urlpatterns": module.__dict__["urlpatterns"]})
else:
    module = __import__("apps.thirdparty.userprofile.urls.en", {}, {}, "urlpatterns")
    globals().update({"urlpatterns": module.__dict__["urlpatterns"]})
