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

import unittest

from tests.data_seeder import seeder

from src.core.spaces.models import Space

from django.contrib.auth.models import User


class TestDataSeeder(unittest.TestCase):
    """Tests the DataSeeder class methods.
    """
    
    def testInstanceIsCreated(self):
        """Tests if the correct instance of a model is generated.
        """
        
        created_model = seeder.seed(Space)
        self.assertTrue(isinstance(created_model, Space))
    
    def testCorrectNumberOfInstancesAreGenerated(self):
        """Tests if correct number of model instances are generated.
        """
        
        count = 5
        actual_list = seeder.seedn(count, Space)
        self.assertEqual(len(actual_list), count)
    
    def testIfInstanceIsGeneratedWithRequiredAttributes(self):
        """Tests if the generated instance has the desired properties.
        """
        
        properties = {
            'name': 'Test Space',
            'description': 'Temporary Description',
            'public': 'False',
        }
        instance = seeder.seed(Space, model_properties=properties)
        self.assertEqual(instance.name, properties['name'])
        self.assertEqual(instance.description, properties['description'])
        self.assertEqual(instance.public, properties['public'])
        #Space.author is a Foreign Key. Since generate_fk is False by default,
        #Space.author should be None as it will not be populated.
        self.assertEqual(instance.author, None)
        self.assertFalse(isinstance(instance.author, User))
    
    def testIfForeignKeyFieldsOfaModelIsPopulated(self):
        """Tests if the foreign key fields of a model is populated if
        generate_fk is set to True
        """
        
        instance = seeder.seed(Space)
        self.assertEqual(instance.author, None)
        
        instance = seeder.seed(Space, generate_fk=True)
        self.assertTrue(isinstance(instance.author, User))
        User.objects.all().delete()