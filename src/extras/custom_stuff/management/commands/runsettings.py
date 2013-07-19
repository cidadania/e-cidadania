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

"""
Change environment according to the parameters.
"""

import os
import sys

from django.core.management.base import BaseCommand, CommandError
from django.core import management


class Command(BaseCommand):

    """
    """
    args = "<settings_file> [development, production]"
    help = "This command will run the django development server with the \
    specified configuration file, which can be 'production' or 'development'."

    def handle(self, *args, **options):

        """
        """
        if args[0] == 'development':
            self.stdout.write('Running development settings...\n')
            management.call_command('runserver', settings="e_cidadania.settings.development", verbosity=0)
        elif args[0] == 'production':
            self.stdout.write('Running production settings...\n')
            management.call_command('runserver', settings="e_cidadania.settings.production", verbosity=0)
        else:
            self.stdout.write("You didn't select a valid option. Valid options are: development, production.\n")
            sys.exit(0)
