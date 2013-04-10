# -*- coding: utf-8 -*-
#
# Copyright (c) 2010-2012 Cidadania S. Coop. Galega
#
# This file is part of e-cidadania.
#
# e-cidadania is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# e-cidadania is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with e-cidadania. If not, see <http://www.gnu.org/licenses/>.

"""
Main URLs for the e-cidadania platform.
"""

from django.conf.urls import *
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from core.views.index import IndexEntriesFeed
from core.views.news import ListNews
from core.views.news import AddPost
from core.views.news import EditPost
from core.views.news import DeletePost
from core.views.news import ViewPost

admin.autodiscover()

# We put here the dictionary with all the packages for translatin JavaScript code
# Please refer to https://docs.djangoproject.com/en/dev/topics/i18n/internationalization/#specifying-translation-strings-in-javascript-code
js_info_dict = {
    'packages': ('apps.ecidadania.debate',),
}

urlpatterns = patterns('',
    # i18n switcher
    (r'^i18n/', include('django.conf.urls.i18n')),
)

urlpatterns += patterns('',

    # Django administration
    (r'^admin/', include(admin.site.urls)),

    # Index
    url(r'^$', 'core.views.index.index_view', name='site-index'),

    # User accounts
    url(r'^accounts/', include('apps.thirdparty.userprofile.urls')),

    # Spaces
    url(r'^spaces/', include('core.spaces.urls')),

    # Invitations
    url(r'^invite/', 'core.views.invite.invite', name='invite'),

    # Explore
    url(r'^explore/$', 'core.views.explore.explore', name='explore'),

    # News (this view of news is only for the index)
    url(r'^news/$', ListNews.as_view(), name='list-site-news'),

    url(r'^news/add/$', AddPost.as_view(), name='add-site-post'),

    url(r'^news/(?P<post_id>\w+)/delete/$', DeletePost.as_view(),
                                            name='delete-site-post'),

    url(r'^news/(?P<post_id>\w+)/edit/$', EditPost.as_view(),
                                          name='edit-site-post'),

    url(r'^news/(?P<post_id>\w+)/$', ViewPost.as_view(),
                                    name='view-site-post'),

    # RSS Feed for the index news ONLY
    url(r'^rss/$', IndexEntriesFeed(), name='site-feed'),

    #(r'^api/', include('e_cidadania.apps.api.urls')),

    # This urls is for the django comments system
    url(r'^comments/', include('django.contrib.comments.urls')),

    (r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict),

    # For smart_selects app
    url(r'^chaining/', include('apps.thirdparty.smart_selects.urls')),

    # This url is for the access to static pages. I hope this doesn't collide
    # with the index view
    url(r'^(?P<slug>[\w\-]+)/', include('apps.ecidadania.staticpages.urls')),

    # WARNING: This URLs aren't supposed to be here, but apparently on development
    # they are needed

    # This url is for comments

    url(r'^comments/', include('django.contrib.comments.urls')),
)

if settings.DEBUG:
    # Serve static files
    urlpatterns += staticfiles_urlpatterns()
    # Serve uploaded files
    urlpatterns += patterns('',
        url(r'^uploads/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    )
