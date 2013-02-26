Creating modules
================

e-cidadania is extensible through modules, which are nothing more than django
apps.

.. warning:: If you want to install modules, you will have to do it on deployment.
             Django does not support modules hotplugging.

Structure
---------

A module is basically a django application which we integrate in e-cidadania. At
this time we advocate for the django default structure in the distribution and file
names.

.. warning:: It's recommended to have expertise in django and python before
             creating a new module.

A module has three basic components, the data model, the view and the
template.

.. note:: Discuss if is worthy to explain the creation of a module.
