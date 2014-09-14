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

__author__ = 'rande'


class StaticHelper(object):
    def __init__(self, router):
        self.router = router

    def url_media_resize(self, media, width=1024):
        return self.router.generate('element.element_path', path=media.path, mr=width)

    def url_media_crop(self, media, size=(200, 200), crop=(0.5, 0.5)):
        return self.router.generate('element.element_path', path=media.path, mf='%s,%s,%s,%s' % (size[0], size[1], crop[0], crop[1]))
