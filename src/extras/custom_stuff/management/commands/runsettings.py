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
