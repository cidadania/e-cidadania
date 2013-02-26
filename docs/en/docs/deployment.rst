Deployment
==========

Installing extra modules
------------------------

e-cidadania comes with a basic set of modules that allow to make a complete
participative process, but you may want to install other modules to have new
features, like forums, chats, or any other kind of django application.

Django does not support module hotplugging, nor e-cidadania. You will have to
install all the modules you think you will need before putting e-cidadania in
production.

Apache 2
--------

.. note:: This section is still on development.

nginx + uWSGI
-------------

.. note:: The installation through uwsgi works for other servers, not just
          nginx, since it's uWSGI who executes the e-cidadania instance while
          the server just serves the static content.

.. note:: This section is still on development.

DreamHost
---------

The instructions for deployment on a DreamHost shared server are too extensive
to include here. You can find them in the `Oscar Carballal blog <http://blog.oscarcp.com>`_
