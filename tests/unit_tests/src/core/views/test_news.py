#/usr/bin/env python
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

from e_cidadania import url_names

from apps.ecidadania.news import models

from tests.test_utils import ECDTestCase


class NewsViewTest(ECDTestCase):
    """Tests the news related views in core.views.news."
    """
    
    def setUp(self):
        super(NewsViewTest, self).init()
    
    def testListNews(self):
        """Tests the view for listing news.
        """
        
        response = self.get(url_name=url_names.LIST_SITE_NEWS)
        self.assertResponseOK(response)
        
    def testAddPost(self):
        """Tests the view for adding news posts.
        """
        # No user is logged in, so we will be redirected to the login page
        response = self.get(url_name=url_names.ADD_SITE_POST)
        # TODO(Praveen): Check for the redirected url
        self.assertResponseRedirect(response)
        
        # Log in a superuser with username as 'admin' and password as `password`
        self.create_super_user(logged_in=True)
        response = self.get(url_name=url_names.ADD_SITE_POST)
        self.assertResponseOK(response)
    
    def testViewPost(self):
        """Tests the view for viewing news posts.
        """
        
        post = self.seed(models.Post)
        url = self.getURL(url_names.VIEW_SITE_POST, kwargs={'post_id': post.id})
        response = self.get(url=url)
        self.assertResponseOK(response)
        
    def testEditPost(self):
        """Tests the view for editing news posts.
        """
        
        post = self.seed(models.Post)
        url = self.getURL(url_names.EDIT_SITE_POST, kwargs={'post_id': post.id})
        self.create_super_user(logged_in=True)
        response = self.get(url)
        self.assertResponseOK(response)
           
    def testDeletePost(self):
        """Tests the view for deleting news posts.
        """
        
        post = self.seed(models.Post)
        url = self.getURL(url_names.DELETE_SITE_POST, 
                          kwargs={'post_id': post.id})
        self.create_super_user(logged_in=True)
        response = self.get(url)
        self.assertResponseOK(response)