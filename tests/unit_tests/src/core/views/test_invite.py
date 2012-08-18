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


class InviteViewTest(ECDTestCase):
    """Tests the invite view in core.views.invite.
    """
    
    def setUp(self):
        self.init()
    
    def testInviteView(self):
        url = self.getURL(url_names.INVITE)
        response = self.get(url)
        self.assertResponseOK(response)
        
        self.create_user('test_user', 'user_pass', logged_in=True)
        response = self.get(url)
        #print self.printResponse(response)
        #print response.context['uri']
        self.assertResponseOK(response)
        
        post_data = {'email_addr': 'test@gmail.com', 'mail_msg':'test'}
        response = self.post(url, data=post_data)
        self.assertResponseOK(response)
