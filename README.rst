e-cidadania
===========

Current version: 0.1.8 beta

e-cidadania is a project to develop an open source application for citizen
participation, which can be used for debates, proposals, trusted voting,
usable by associations, companies and administrations.

The e-cidadania objective is to provide a way to make a full participation
process on internet, or even use it as a complement to in person participative
processes.

Installation
------------

Since e-cidadania 0.1.5 we include an automated buildout system. If you want to
install it to do testing or development you should see
`these instructions <https://github.com/cidadania/e-cidadania/blob/gsoc2012/docs/en/dev/environment.rst>`_

If you don't want to create an isolated development environment:

* Download the source code from git, or from the official webpage.
* You need to install the python packages specified in requirements.txt for
  e-cidadania, you can do it with pip::

    sudo pip install -r requirements.txt

* Configure *src/e_cidadania/settings/production.py to you desire.
* Generate the database with::

    python manage.py syncdb

* Copy all the static files::

    python manage.py collectstatic

* Run the development server

    python manage.py runserver

Demonstration
-------------

There is a demo running in the website http://demo.ecidadania.org.

Development
-----------

**We need developers! If you want to join us, send an email to oscar.carballal AT cidadania DOT coop**

Development and bugtracking is done through `code.ecidadania.org <http://code.ecidadania.org>`_

Getting help
------------

 * `Documentation <http://code.ecidadania.org/wiki/Documentation>`_ e-cidadania documentation.
 * `Mailing lists <http://code.ecidadania.org/wiki/MailingLists>`_ global and local.
 * `Social networks <http://code.ecidadania.org/wiki/SocialNetworks>`_ where e-cidadania present.
 * `Website <http://ecidadania.org>`_ e-cidadania official website.
 * `IRC channels <http://webchat.freenode.net>`_ #ecidadania-dev and #ecidadania for e-cidadania.

Useful information
------------------

 * `Design concepts <http://code.ecidadania.org/wiki/DesignConcepts>`_ design concepts, this are the guides to follow when developing.
 * `Releases <http://code.ecidadania.org/wiki/Releases>`_ version roadmap. This is where we stablish the features, release dates and other things of every version.

Collaborate
-----------

* **Developing** You can take the last code from the repository and experiment with it. When you're done, you can send us a "Merge request". 

* **Documenting** Right now the documentation is a bit insufficient. If you want to document e-cidadania, feel free to do it. We use Sphinx (1.1.3) to generate the documents.

* **Translating** e-cidadania achieves to be international. If you want to translate it to your language just follow the steps in the documentation an send your catalog to us, we will include it ASAP.

* **Bug reporting** You can report the bugs you find in the application in this trac: http://code.ecidadania.org
