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

import os
import re
from setuptools import setup, find_packages


setup(
    name = 'e-cidadania',
    description = ("e-cidadania is a project to develop an open source "
                   "application for citizen participation, usable by "
                   "associations, companies and administrations."),
    version = '0.1.9',
    packages = find_packages(exclude=['parts']),
    author = 'Oscar Carballal Prego',
    url = 'http://ecidadania.org',
    license = '3-clause BSD',
    install_requires = [
        'django==1.5.1',
        'PIL',
        'python-dateutil==1.5',
        ],
    tests_require=[
        'nose',
        'django-nose',
        'coverage',
        'nose-cov',
        ],
    entry_points = {'console_scripts': ['check-quality = tests.run:main',
                                       ],
                   },
    include_package_data = True,
    zip_safe = False,
    )
