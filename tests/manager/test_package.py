#
# Copyright 2014 Thomas Rabaix <thomas.rabaix@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import unittest
import element.manager

class PackageTest(unittest.TestCase):

    def test_is_uuid(self):

        self.assertTrue(element.manager.is_uuid("fca0ea55-c21b-186e-fe6924a5"))
        self.assertFalse(element.manager.is_uuid("FCA0EA55-C21B-186E-FE6924A5"))
        self.assertFalse(element.manager.is_uuid("salut-comment-ca-ca-bien?"))
