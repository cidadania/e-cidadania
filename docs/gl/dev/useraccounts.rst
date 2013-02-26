User accounts
=============

The user account system in e-cidadania is abased on the django *auth* module and
in django-userprofile, created by James Bennet.

It might be that for other installations of e-cidadania you need other user
data instead of the provided by the e-cidadania default installation. In
that case you can modify the data model of the user.

The file containing the data model for the user profile is found in
`apps/accounts/models.py`. All the fields can be replaced except `age` and
`spaces`.

.. note:: Remember, after modifying the data model you will need to rebuild
          your database. We encourage you to have some application for
          database schema migration like *django-evolution*

Users are spearated in two parts. One of them is the django user account
created by the *auth* module and the other is the *profile* object
containing all the profile data for the user.

Users can be created without profile, but once you try to create a profile
you will have to fill it and it will be linked to the user.

Public profiles
---------------

Users have a public zone in their profiles, which will show the data they
want to show.

The public data will be visible to anyone visiting the profile, platform
user or not.

.. note:: Be careful with the personal data you show on the net.

.. warning:: Currently the data on the public profile is not configurable by
             the users. This is expected to change in e-cidadania 0.1.5.
