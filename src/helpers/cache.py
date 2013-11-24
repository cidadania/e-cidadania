# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Clione Software
# Copyright (c) 2010-2013 Cidadania S. Coop. Galega
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
This file contains functions to help with caching.
"""

# Django's cache module
from django.core.cache import cache
from django.utils import six

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

    if not isinstance(key, six.string_types):
        raise TypeError('key must be str or a unicode string')

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
