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
Default settings for the e-cidadania project. This settings can be overriden by
the development and production files. They also can add new settings to this file.

Plase refer to the 'configuration' section of the documentation for guidance.
"""

import os

# e-cidadania version and current status
__version__ = "0.1.8"
__status__ = "beta"

# Get the current working directory so we can fill automatically other variables.
cwd = os.path.dirname(os.path.realpath(__file__)).strip('settings')
#print "Current working dir: %s" % cwd

# Extending the user profile a bit more
AUTH_PROFILE_MODULE = "accounts.UserProfile"
ACCOUNT_ACTIVATION_DAYS = 2
LOGIN_REDIRECT_URL = '/accounts/'

# Languages for the platform.
LANGUAGES = (
    ('es_ES', 'Español'),
    ('en_GB', 'English'),
    ('gl_ES', 'Galego'),
    ('fr_FR', 'Français'),
    ('mk_MK', 'Makedonski')
)

LOCALE_PATHS = (
    cwd + '/templates/locale',
)

SITE_ID = 1
USE_I18N = True
USE_L10N = True

# Calendar
FIRST_WEEK_DAY = 0 # '0' for Monday, '6' for Sunday

# Configuration related to media and static content directories
MEDIA_ROOT = cwd + '/uploads/'
#print "Media root: %s" % MEDIA_ROOT
MEDIA_URL = '/uploads/'
STATIC_ROOT = cwd + '/static/'
#print "Static root: %s" % STATIC_ROOT
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = STATIC_URL

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

STATICFILES_DIRS = (
    (cwd + '/static_files/'),
)

FILE_UPLOAD_HANDLERS = (
    "django.core.files.uploadhandler.MemoryFileUploadHandler",
    "django.core.files.uploadhandler.TemporaryFileUploadHandler",
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '8nwcwmtau*bnu0u=shmdkda^-tpn55ch%qeqc8xn#-77r8c*0a'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
)

MIDDLEWARE_CLASSES = (
    # GZipMiddleware compresses content for modern browsers
    'django.middleware.gzip.GZipMiddleware',
    # ConditionalGetMiddleware adds support for modern browsers to conditionaly 
    # GET responses
    'django.middleware.http.ConditionalGetMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'e_cidadania.urls'
APPEND_SLASH = True

TEMPLATE_DIRS = (
    (cwd + '/templates'),
)

# We separate the applications so we can manage them through scripts
# Please do not touch this unless you know very well what you're doing

DJANGO_APPS = (
    # This list is from the builtin applications in django that are used in
    # e-cidadania
    'core.prismriver',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.comments',
    'django.contrib.admin',
    'django.contrib.comments',
)

# Stablish message storage
MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

THIRDPARTY_APPS = (
    # This list is from the third party software included in e-cidadania or
    # system-wide dependencies.
    'apps.thirdparty.smart_selects',
    'apps.thirdparty.userprofile',
    'apps.thirdparty.tagging',
)

ECIDADANIA_MODULES = (
    # Modules created for e-cidadania and installed by default. You can add
    # here your own modules
    'core.spaces',
    'apps.ecidadania.accounts',
    'apps.ecidadania.proposals',
    'apps.ecidadania.news',
    'apps.ecidadania.debate',
    'apps.ecidadania.staticpages',
    'apps.ecidadania.cal',
    'extras.custom_stuff',
    'apps.ecidadania.voting',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# Combine all the apps in the django variable INSTALLED_APPS
INSTALLED_APPS = DJANGO_APPS + THIRDPARTY_APPS + ECIDADANIA_MODULES

# Activate the new url syntax in django 1.3 which will be
# compatible till 1.5
import django.template
django.template.add_to_builtins('django.templatetags.future')
