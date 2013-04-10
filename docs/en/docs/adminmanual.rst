Administration manual
=====================

This is a small introductory manual to teach you about how to use e-cidadania
without messing everything up :).

Administration panel
---------------------


Users
-----

Restricting user registration
`````````````````````````````
.. note:: This behaviour will change on e-cidadania 0.2

e-cidadania has a basic automated registration system that the administrator can
activate or deactivate at his own will. By default, e-cidadania comes with
registration activated, but if for some reason the administrator wants to block
that registration system (passing to manual mode) he just has to activate when he considers removing the comment symbol (sharp).

*apps/userprofile/urls/en.py:107*::

   # url(r'^register/$', register, name='signup'),

If the platform is well set up, the registration system should take care of
everything.

Permissions
```````````
Permissions in e-cidadania are inherited directly from the django auth system.
This way we have group based permissions and user based permissions.

.. note:: e-cidadania 0.2 will have a row-level permission system.

There are four basic permissions:

**Creation**
  Depending on the moderation grade that you have been given, you can add simple
  content or more complex. The highest moderation levels have a very high detail
  grade when adding content.

**Editing**
  The editing task is similar to creation, it will return a formulary with the
  current data based on your permission level.

**Deletion**
  Usually in forums a moderator can delete user entries. In e-cidadania that is
  not the objective. User generated content must be preserved, it only can be
  deleted by platform administrators.
  
**Move note**
  This permission is for the debate system. IT allows or restricts the user
  capability of moving notes across the debate. The notes moving task is reserved
  for the space administrators.
  
Add/Remove
''''''''''

Groups
``````

Groups are a massive way to give permissions to people. In this version groups will
be a way to group people inside the spaces, except that for any reason you'll have
to give them another permission for a specific task.

Adding/Removing groups
''''''''''''''''''''''

Adding people to groups
'''''''''''''''''''''''

Spaces
------

What are they
`````````````

How spaces work
```````````````

Modules
-------

Debates
```````

Debate creation
'''''''''''''''

Moderation
''''''''''

Proposals
`````````

Creating a proposal set
'''''''''''''''''''''''

How to merge proposals
''''''''''''''''''''''

Voting
``````

Creating a set
''''''''''''''

Moderation
''''''''''

Frequent errors
---------------

The most frequest errors are due to the server or a bad administrator management
in the groups/permission case.

