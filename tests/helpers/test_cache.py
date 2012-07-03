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


from django.core.cache import cache

from core.spaces.models import Space

from src.helpers import cache as cache_helper

from tests.test_utils import ECDTestCase



class CacheHelperTest(ECDTestCase):
    """Tests the cache helper functions.
    """
    
    def setUp(self):
        self.init()
        
    def testGetOrInsertObjectInCache(self):
        """
        Tests the get_or_insert_object_in_helpers.cache.
        """
        
        
        space_props = {'url': 'test_space', 'name': 'some_name'}
        #print Space.__class__.__name__
        space_key = cache_helper._get_cache_key_for_model(Space, 'test_space')
        expected = None
        actual = cache.get(space_key)
        self.assertEqual(expected, actual)
        
        space = Space(**space_props)
        space.save()
        expected = space
        actual = cache_helper.get_or_insert_object_in_cache(Space, 
                                                            space.url, url=space.url)
        self.assertEqual(expected, actual)
        
        cache.delete(space_key)
        self.assertEqual(cache.get(space_key), None)
        expected = space
        actual = cache_helper.get_or_insert_object_in_cache(Space, 
                                                            space.url, url=space.url)
        self.assertEqual(expected, actual)
        