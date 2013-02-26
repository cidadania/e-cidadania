from django.conf.urls.defaults import *

urlpatterns = patterns('', url(r'^$', 'prismriver.dashboard.views.dashboard'))