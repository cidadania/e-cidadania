#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This script automates the creation of all the language catalogs for a django
project, creating both standard and JS catalogs.
"""

import sys
import os
import subprocess
import argparse

__author__ = "Oscar Carballal Prego <oscar.carballal@cidadania.coop>"
__license__ = "GPLv3"
__version__ = "0.6"


class Language():

    """
    Language class.
    """
    def __init__(self):

        """
        Store all the applications and languages installed in the platfom
        """
        # Get current work directory and add it to sys.path so we can import
        # the project settings.
        self.cwd = os.getcwd()  # Remove scripts directory just in case
        sys.path.append(self.cwd)

        # Get the languages configured in settings.py and the installed
        # e-cidadania modules. If we can't get the settings module, abort execution.
        try:
            import e_cidadania.settings as settings
        except:
            sys.exit("\nCould not import the settings module. Aborting execution.\n\
Probable cause: the script is not being executed from the project root (usually src/).\n")

        # You must put here the name off you applications variable in the form
        # "settings.YOURVARNAME"
        APPLICATIONS = settings.ECIDADANIA_MODULES

        self.applications = APPLICATIONS
        self.languages = settings.LANGUAGES
        self.appnames = []
        self.appdirs = []

        # We are going to add all the applications of the project, and create
        # a dictionary with appname:appdir values
        print "\n >> Populating variables with applications...\n"
        for app in self.applications:
            appdata = app.split('.')  # Separate all components
            # appdata.pop(0) # Remove project name, it's useless. This was for django <= 1.3
            app_path_list = appdata  # This will leave us with an useful route to the application
            app_path = '/'.join(app_path_list)
            appname = app_path_list[-1]  # Get the application name (last value)
            self.appnames.append(appname)
            self.appdirs.append(app_path)

        # When we exit the for loop, create a dictionary with appname:app_path
        self.appDict = dict(zip(self.appnames, self.appdirs))
        print self.appDict

    def _iterator(self, command, action):

        """
        This method iterates over the applications and languages executing the
        command specified in the call.
        """
        for app, appdir in self.appDict.items():
            os.chdir(self.cwd + '/' + appdir)
            print '\n>> %s language catalog: %s' % (action, app)
            for lang in self.languages:
                a = subprocess.Popen(command + '-l %s' % (lang[0]), shell=True)
                subprocess.Popen.wait(a)

        print '\n>> %s site root language catalog.' % (action)
        os.chdir(self.cwd + '/e_cidadania')
        for lang in self.languages:
            if action is not "Compiling":
                a = subprocess.Popen(command + "-i 'apps/*' -l %s" % (lang[0]), shell=True)
            else:
                a = subprocess.Popen(command + "-l %s" % (lang[0]), shell=True)
            subprocess.Popen.wait(a)

    def make(self):

        """
        Generate the language catalogs for the application and site root.
        """
        # Spit out the information
        print "\n>> Languages to generate:"
        for lang in self.languages:
            print ' - ' + lang[1]

        print "\n>> Installed applications:"
        for app in self.appDict.keys():
            print ' - ' + app

        self._iterator('django-admin.py makemessages ', 'Generating')
        self._iterator('django-admin.py makemessages -d djangojs ', 'Generating JavaScript')

    def compile(self):

        """
        Compile all the language catalogs.
        """
        # Spit out the information
        print "\n>> Languages to generate:"
        for lang in self.languages:
            print ' - ' + lang[1]

        print "\n>> Installed applications:"
        for app in self.appDict.keys():
            print ' - ' + app

        self._iterator('django-admin.py compilemessages ', 'Compiling')

    def clean(self):

        """
        Removes the language installed catalogs in the platform, leaving the
        locale directories clean for new catalogs.
        """
        print '\n>> WARNING: This command will remove ALL the language catalogs, having to rebuild and translate them all.'
        raw_input('\n Continue? (Ctrl-C to quit)')
        for app, appdir in self.appDict.items():
            os.chdir(self.cwd + '/' + appdir)
            print '\n>> Cleaning language catalogs for %s' % (app)
            for lang in self.languages:
                a = subprocess.Popen('rm -rf locale/%s' % (lang[0]), shell=True)
                subprocess.Popen.wait(a)

        print '\n>> Cleaning site root language catalogs'
        os.chdir(self.cwd)
        for lang in self.languages:
            a = subprocess.Popen('rm -rf locale/%s' % (lang[0]), shell=True)
            subprocess.Popen.wait(a)

lang = Language()
parser = argparse.ArgumentParser(description='e-cidadania language catalog generator. This script manages all the .po and .mo files from templates, python code and javascript i18n (if used).')
subparser = parser.add_subparsers()
parser_make = subparser.add_parser('make', help='Create all the language catalogs for translation including JavaScript.')
parser_make.set_defaults(func=lang.make)

parser_compile = subparser.add_parser('compile', help='Compile all the language catalogs for use.')
parser_compile.set_defaults(func=lang.compile)

parser_clean = subparser.add_parser('clean', help='Delete all the language catalogs. After this you will have to rebuild the catalogs and translate them.')
parser_clean.set_defaults(func=lang.clean)


args = parser.parse_args()
args.func()
