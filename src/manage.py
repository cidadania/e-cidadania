#!/usr/bin/env python
import os
import sys

os.environ.setdefault('LANG', 'en_US')

if __name__ == "__main__":
    manage_cwd = os.getcwd()
    sys.path.insert(0, manage_cwd + '/e_cidadania')
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "e_cidadania.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
