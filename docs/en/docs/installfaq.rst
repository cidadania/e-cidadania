Installation FAQ
================

.. note:: If you find some frequent question that might be important please send it via mail to info@ecidadania.org or create a new ticket in the bugtracker describing it.

These are some of the usual cases you can find while installing e-cidadania.

I have installed PIL, but e-cidadania gives errors about a JPEG decoder
----------------------------------------------------------------------
You have installed PIL without support for *jpglib*, a library that helps PIL understand images. You need to install the package *libjpeg-dev* or the equivalent in your distribution.

I can't compile PIL, it says "Python.h: The file does not exist"
----------------------------------------------------------------
You will have to install the Python development libraries in your systems, they provide the necessary files for PIL and other tools to compile. The package is *python-dev* (or *python-devel*) or the equivalent in your distribution.

The buildout crashes continuosly because it can't reach the internet to download the packages
---------------------------------------------------------------------------------------------
This is actually a problem of the *pip* servers, they have very annoying downtimes. Please try again later :)

The platform gives errors about a "nose" package
------------------------------------------------
There can be a lot of reason for this to happen, but the usuals are:

1) You're trying to work in production with settings from development
2) You're trying to run e-cidadania from a directory that is not /src

.. note:: More reasons to come.

