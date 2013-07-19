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

from e_cidadania.settings.defaults import *

# Registration mail settings
# EMAIL_HOST = ""
# EMAIL_PORT=
# EMAIL_HOST_USER=""
# EMAIL_HOST_PASSWORD=""
DEFAULT_FROM_EMAIL = ""
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

# Change this to your working domain! If this variable is empty, django
# will return an error 500
#ALLOWED_HOSTS = ['*'] # This allows any host. INSECURE!
ALLOWED_HOSTS = []

# Make this unique, and don't share it with anybody.
SECRET_KEY = '8nwcwmtau*bnu0u=shmdkda^-tpn55ch%qeqc8xn#-77r8c*0a'

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
