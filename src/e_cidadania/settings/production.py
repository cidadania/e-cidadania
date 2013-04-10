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

from e_cidadania.settings.defaults import *

# Registration mail settings
# EMAIL_HOST = ""
# EMAIL_PORT=
# EMAIL_HOST_USER=""
# EMAIL_HOST_PASSWORD=""
# DEFAULT_FROM_EMAIL = ""
# EMAIL_USE_TLS = True

# Time and zone configuration
TIME_ZONE = 'Europe/Madrid'
LANGUAGE_CODE = 'es-es'

# Cache backend.
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake'
    }
}

# Who will we alert?
ADMINS = (
    ('YourAdmin', 'youradmin@adminmail.com'),
)
MANAGERS = ADMINS


# Make this unique, and don't share it with anybody.
SECRET_KEY = '8nwcwmtau*bnu0u=shmdkda^-tpn55ch%qeqc8xn#-77r8c*0a'

# Database configuration. Default: sqlite3
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'e_cidadania/db/production.db',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}
