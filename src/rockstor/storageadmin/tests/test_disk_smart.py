
"""
Copyright (c) 2012-2013 RockStor, Inc. <http://rockstor.com>
This file is part of RockStor.

RockStor is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published
by the Free Software Foundation; either version 2 of the License,
or (at your option) any later version.

RockStor is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

from rest_framework import status
from rest_framework.test import APITestCase
import mock
from mock import patch
from storageadmin.tests.test_api import APITestMixin

class DiskSmartTests(APITestMixin, APITestCase):
    fixtures = ['fix1.json']
    BASE_URL = '/api/disks/smart'

    @classmethod
    def setUpClass(cls):
        super(DiskSmartTests, cls).setUpClass()
    
                      
    @classmethod
    def tearDownClass(cls):
        super(DiskSmartTests, cls).tearDownClass()

    def test_get(self):
        
        # get base URL
        response = self.client.get('%s/info' % self.BASE_URL)
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK, msg=response.data)
         
    def test_post_requests(self):
        
        # invalid disk
        response = self.client.post('%s/info/invalid' %self.BASE_URL)
        self.assertEqual(response.status_code,
                         status.HTTP_500_INTERNAL_SERVER_ERROR, msg=response.data)
        e_msg = ('Disk: invalid does not exist')
        self.assertEqual(response.data['detail'], e_msg)
        
        # invalid command
        response = self.client.post('%s/invalid/sdd' %self.BASE_URL)
        self.assertEqual(response.status_code,
                         status.HTTP_500_INTERNAL_SERVER_ERROR, msg=response.data)
        e_msg = ('Unknown command: invalid. Only valid commands are info and test')
        self.assertEqual(response.data['detail'], e_msg)
        
        # unsupported self test
        data = {'test_type':'invalid'}
        response = self.client.post('%s/test/sdd' %self.BASE_URL, data=data)
        self.assertEqual(response.status_code,
                         status.HTTP_500_INTERNAL_SERVER_ERROR, msg=response.data)
        e_msg = ('Unsupported Self-Test: invalid')
        self.assertEqual(response.data['detail'], e_msg)
        
        # test command
        data = {'test_type':'short'}
        response = self.client.post('%s/test/sdd' %self.BASE_URL, data=data)
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK, msg=response.data)
        
        # happy path
        response = self.client.post('%s/info/sdd' %self.BASE_URL)
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK, msg=response.data)
        
        
             

