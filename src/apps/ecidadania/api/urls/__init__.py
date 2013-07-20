# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Clione Software
# Copyright (c) 2010-2013 Cidadania S. Coop. Galega
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.conf.urls import patterns, url, include
from rest_framework import routers
from apps.ecidadania.api.views.accounts import UserViewSet, GroupViewSet


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns = patterns('',

    url(r'^', include(router.urls)),

    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),

    # url(r'^debates/', include('apps.ecidadania.api.urls.debates', namespace='debate_api')),

    # This one should go on the spaces api
    # url(r'^news/', include('apps.ecidadania.api.urls.news', namespace='news_api')),

    url(r'^spaces/', include('apps.ecidadania.api.urls.spaces', namespace='spaces_api')),

    # url(r'^proposals/', include('apps.ecidadania.api.urls.proposals', namespace='rest_framework')),

    # url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),

    # url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),

    # url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),

)
