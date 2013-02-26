Installation
============

e-cidadania installation is very simple and is done almost in the same as any
other django platforms.

Downloading platform
--------------------

Official download page
``````````````````````

The are several ways to download e-cidadania. The most simple of them is going
to the `downloads <http://ecidadania.net/en/download/>`_ page in the website
and download the latest stable or development versions, ready to use.

GitHub packages
```````````````

Other way of downloading it is through the Github downloads page, which
autogenerates a .zip and .tar.gz files based on the repository tags. You can
find it in::

    https://github.com/cidadania/e-cidadania/tags

From repository
```````````````

See :ref:`dev-version`

Stable version
``````````````

You can find the latest stable version in the download page in ecidadania.org::

    http://ecidadania.net/en/downloads

.. _dev-version:

Development version
```````````````````

Development version is available through various places. We use `GIT <http://git-scm.com/>`_
as version control system, so you will have to install it in your computer.

    **GitHub** *(official repository)*::

        git clone git://github.com/cidadania/e-cidadania.git

    **Gitorious:** *(secondary repository)*::

        git clone git://gitorious.org/e-cidadania/mainline.git

    **Repo.or.cz** *(official mirror)*::

        git clone git://repo.or.cz/e_cidadania.git

Installing
----------

.. warning:: Since e-cidadania 0.1.5 we included an automated buildout system. If you are going to develop in e-cidadania you should take a look to the :doc:`../dev/environment`.

The installation process for e-cidadania is quite simple.

Requirements
````````````
- Apache, nginx, or any other web server with CGI suppport
- FastCGI, uWSGI, Passenger or other CGI.

**Dependencies**

- Python 2.7.x
- django 1.4.x
- PIL *(Python Imaging Library)*
- python-datetime *(version 1.5)*
- django-tagging
- django-grappelli
- feedparser
- pyyaml

You can install all the required dependencies automatically with this command::

    # pip install -r requirements.txt

Most of the requirements are automatically installed this way, but there are
some packages that need to be installed via the system packages, for example:

* PIL

.. warning:: There are reported errors for people that tried to install PIL from
             pip instead from the official system package. The problem is due to
             the lack of some features of PIL needed in e-cidadania.

Platform
````````
There isn't a proper installation process in e-cidadania, you just have to copy
the files to you preferred installation directory.

If you are going to use it in production, or you just want to give e-cidadania
a try follow this steps:

.. note:: e-cidadania comes preconfigured for a development environment. You
          will have to set the DEBUG flag to **False** in
          *src/e_cidadania/settings/__init__.py*
::

    $ ./manage.py syncdb # This will create all the database objects
    $ ./manage.py collectstatic # This will copy all the static content to *static/*
    $ ./manage.py runserver

This last command will execute the development server in the port 8000 of your
machine, so you just need to type **localhost:8000" inside a web browser.

Now you can continue to :doc:`configuration`
