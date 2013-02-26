Creating the environment
========================

For the people wanting to develop e-cidadania, we recommend to setup a new
environment using buildout.

Steps
-----

Below are the steps explained in a greater detail.

* Clone the official git repository of e-cidadania. ::

    $ git clone https://github.com/cidadania/e-cidadania

* cd into the e-cidadania folder just cloned. ::

    $ cd e-cidadania

* Just to be sure, when you do a ls, you should find a bootstrap.py python 
  module and a buildout.cfg buildout configuration file. ::

    ~/e-cidadania$ ls
    bootstrap.py  buildout.cfg  docs  __init__.py  README.rst  setup.py  src  tests

* Now run the bootstrap.py script with your system python. ::

    ~/e-cidadania$ python bootstrap.py

* If the bootstrapping procedure runs successfully, you will see the following
  output in the terminal. ::

    ~/e-cidadania$ python bootstrap.py
    Downloading http://pypi.python.org/packages/2.7/s/setuptools/setuptools-0.6c11-py2.7.egg
    Creating directory '/home/user/e-cidadania/bin'.
    Creating directory '/home/user/e-cidadania/parts'.
    Creating directory '/home/user/e-cidadania/eggs'.
    Creating directory '/home/user/e-cidadania/develop-eggs'.
    Getting distribution for 'setuptools'.
    Got setuptools 0.6c12dev-r88846.
    Generated script '/home/user/e-cidadania/bin/buildout'.

* Run the buildout script created in e-cidadania/bin ::

    ~/e-cidadania$ bin/buildout
        
Now buildout will run and download all the packages required for development
in the e-cidadania.eggs folder and add them to the python path of the
bin/django script which will be created after buildout runs successfully.

buildout will download the django framework itself and other packages as
defined in buildout.cfg. bin/django is a wrapper around manage.py and works
exactly the same way as manage.py and it must be used to run any django
management commands while you are in the development environment.
  
.. warning:: On some linux systems, running bin/buildout fails when installing
          PIL. The solution is to install python-imaging and in some
          environments python-devel too. Install python-imaging and re-run
          bin/buildout.

If the step above completes sucessfully, you will find a number of scripts in
bin folder. Make sure that you have django and python in the bin folder.
  
* Now cd into the src folder. ::
  
    ~/e-cidadania$ cd src
  
* Generate the database::

    ~/e-cidadania/src$ ../bin/django syncdb

* Copy all the static files::

    ~/e-cidadania/src$ ../bin/django collectstatic

* Run the development server::

    ~/e-cidadania/src$ ../bin/django runserver

That's it!

Running the tests
-----------------

We have drifted away from the Django way of keeping the tests with the source
itself. All the tests are in a single folder called 'tests' which you can find
at the root of e-cidadania. By default, the test runner is configured to run
all the tests present in the test folder.


* To run all the tests::

    ~/e-cidadania$ bin/django test

or when you are in src::

    ~/e-cidadania/src$ ../bin/django test

* To run the tests with coverage::

    ~/e-cidadania$ bin/django test --with-cov

or when you are in src::

    ~/e-cidadania/src$ bin/django test --with-cov

