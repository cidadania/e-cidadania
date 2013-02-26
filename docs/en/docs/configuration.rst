Configuration
=============

The e-cidadania platform is almost ready-to-use after unpacking, but you will
have to edit the `settings.py` file if you want to install it in production. We
explain here all the settings realted with the initial configuration of
e-cidadania. If you want more detailed information about the settings, please
take a look at the official django documentation at
`http://docs.djangoproject.com`_

The e-cidadania setting have been splitted into four major files::

    settings/
        __init__.py
        defaults.py
        development.py
        production.py

__init__
--------

This file loads one configuration or another based on the *DEBUG* flag. You
have to set this first.

**DEBUG** (boolean)
    You have to set this value to *True* or *False* depending if you are using
    the platform or want to debug the e-cidadania platform.

defaults
--------

This file stablishes the common settings across the both environments. Most of
this settings are e-cidadania specific, we will specify here the ones you can
modify safely.

**SECRET_KEY** (hash)
    It's **obligatory** to modify this value before deployment. This key is
    used for generating the CSRF and some other security features in django.

**MEDIA_ROOT** (directory)
    e-cidadania comes with this directory set by default for development but
    you will have to modify it to suit the directory where you media content
    or user uploaded content will be.

**MEDIA_URL** (URL slug)
    This will be the accesible URL for the media content. e-cidadania comes
    set to "uploads/" but you can modify it at any time.

**STATIC_ROOT** (directory)
    This directory works the same as MEDIA_ROOT but for static content
    (JavaScript, CSS, images, etc.). e-cidadania comes with it set by default
    for development but you will have to modify it to where you static content
    will be stored.

**STATIC_URL** (URL slug)
    This will be the accesible URL for the static content. e-cidadania comes
    with it set to "static/" but you can modify it at any time.

**ACCOUNT_ACTIVATION_DAYS** (integer)
    This is the number of days that you will allow to your users for verifying
    their accounts after they registered into the platform. *Default: 2*

**FIRST_WEEK_DAY** (integer)
    Just in case your country calendars don't start in Monday, you have the
    possibility of making the week start on Sunday (put 1 instead of 0).
    *Default: 0 (Monday)*
    
This are the main settings that you will have to modify to make the deployment
of e-cidadania, you shouldn't need to modify the rest unless you want a very
specific deployment, in which case we recommend you to read the django
documentation about the settings.

development and production
--------------------------

*development.py* and *production.py* are minor configuration files with all the
parameters we think you will need to make a development or production server.

Database
````````

**Configuring the database**::

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db/sqlite.db',
            'USER': '',
            'PASSWORD': '',
            'HOST': '',
            'PORT': '',
        }
    }
    
First of all will be to set up the database. By default e-cidadania is set up to
use a local SQLite3 database, which will be useful to make tests, but we don't
recommend to use it in production.

An example of a database on a DreamHost shared server is this::

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'superb_database',
            'USER': 'databaseadmin',
            'PASSWORD': 'somepassword',
            'HOST': 'mysql.myserver.org',
            'PORT': '',
        }
    }

**DEBUG** (Boolean True, False)
    The debug mode is meant for development only, it overrides some of the
    security systems of django and offers a detailed output when django crashes.
    This setting is meant to not be modified by the user.
    
**TIMEZONE**
    Time zone that e-cidadania will use as default.

**LANGUAGE_CODE**
    Main language that e-cidadania will use for the users. It uses the language
    code format, p.e. en-US (United States english)
    
**CACHES**
    Configure the cache backcend for django. Please refer to the django
    documentation so you can select a cache according to your needs.

**ADMINS** (python dictionary)
    List of *name*, *email* tuples with the administrators data. This is used
    in case e-cidadania has to send some report or django sends an error log.

**EMAIL SETTINGS**
    The email settings are pretty straightforward, so we will not explain them here.
    
    .. warning:: Django 1.4 still doesn't have nice support for autoverified
                SSL emails, you will need to use secure (but not handshaked)
                TLS email addresses.

Extensions
----------

.. note:: This section is still on development.

Extensions are django applications that you can attach to e-cidadania to improve
its functionalities. Currently e-cidadania doesn't support a hotplug plugin
system.

You can continue now to :doc:`deployment`