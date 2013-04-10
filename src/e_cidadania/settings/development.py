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

# Import all the settings.defaults settings
from e_cidadania.settings.defaults import *

# Registration mail settings. Please use a different mail server and account
# during development than in production.
# EMAIL_HOST = ""
# EMAIL_PORT= 25
# EMAIL_HOST_USER= ""
# EMAIL_HOST_PASSWORD= ""
# DEFAULT_FROM_EMAIL = ""
# EMAIL_USE_TLS = True
EMAIL_HOST = "mail.ecidadania.org"
EMAIL_PORT= 25
EMAIL_HOST_USER="info@ecidadania.org"
EMAIL_HOST_PASSWORD="MbNu?@HWfBRvKhr"
DEFAULT_FROM_EMAIL = "info@ecidadania.org"
SERVER_EMAIL = "info@ecidadania.org"
EMAIL_USE_TLS = True


# Time and zone configuration
TIME_ZONE = 'Europe/London'
LANGUAGE_CODE = 'en-gb'

# Cache backend. Default: local memory storage
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake'
    }
}

# Who will we alert?
ADMINS = (
    ('YourAdmin', 'user@host.com'),
)
MANAGERS = ADMINS

# Database configuration. Default: sqlite3
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'e_cidadania/db/development.db',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

# Debug toolbar settings. By default is commented, if you want to activate it,
# you will have to install django-debug toolbar and uncomment all this section.
# INTERNAL_IPS = ('127.0.0.1',)
# MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
# ECIDADANIA_MODULES += ('debug_toolbar',)

TEST_APPS = (
    # Apps which form a part of the testing framework of e-cidadania.
    'django_nose',
)

# Override django's default test runner to use Nose test runner instead.

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = ['tests.unit_tests', '-s', '--cov-report', 'term-missing']

NOSE_PLUGINS = [
    'tests.nose_plugins.DatabaseFlushPlugin',
]

INSTALLED_APPS += TEST_APPS
