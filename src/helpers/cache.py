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
This file contains functions to help with caching.
"""

# Django's cache module
from django.core.cache import cache

# Cached models
from core.spaces.models import Space

# Response types
from django.shortcuts import get_object_or_404

# Tries to get the object from cache
# Else queries the database
# Else returns a 404 error


def _get_cache_key_for_model(model, key):
    """
    Returns a unique key for the given model.

    We prefix the given `key` with the name of the `model` to provide a further
    degree of uniqueness of keys across the cache.
    """

    if not isinstance(key, basestring):
        raise TypeError('key must be  str or a unicode string')

    return model.__name__ + '_' + key


def get_or_insert_object_in_cache(model, key, *args, **kwargs):
    """
    Returns an instance of the `model` stored in the cache with the given key.
    If the object is not found in the cache, it is retrieved from the database
    and set in the cache.
    """

    actual_key = _get_cache_key_for_model(model, key)
    return_object = cache.get(actual_key)

    if not return_object:
        return_object = get_object_or_404(model, *args, **kwargs)
        cache.set(actual_key, return_object)

    return return_object
