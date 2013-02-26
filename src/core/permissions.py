# -*- coding: utf-8 -*-
#
# Copyright (c) 2010-2012 Cidadania S. Coop. Galega
#
# This file is part of e-cidadania.
#
# e-cidadania is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# e-cidadania is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with e-cidadania. If not, see <http://www.gnu.org/licenses/>.

"""
This file contains various check functions for the permission system integrated
inside the spaces module and also some checks for the django auth
system.
"""

def has_operation_permission(user, space, object_permission, allow):

    """
    Checks if the user has all the required permissions to perform a operation.
    :user: User object
    :space: Space object
    :object_permission: Specific operation permission 
    :allow: List of users to allow, can be: admins, mods or users
    """
    return has_all_permissions(user) \
    or (has_space_permission(user, space, allow) \
    and user.has_perm(object_permission))


def has_space_permission(user, space, allow=[]):

    """
    Check if the user is in one of the fields that regulate permissions
    on the space, and if the anonymous users are allowed. The function checks
    the *allow* list and checks one by one until it finds one that returns True.

    Arguments

    :user: User object
    :space: Space object
    :allow: List of users to allow, can be: admins, mods or users

    .. versionadded:: 0.1.6

    """
    for role in allow:
        group = getattr(space, role)
        if user in group.all():
            return True
        else:
            pass

def has_all_permissions(user):
    return user.is_staff or user.is_superuser
